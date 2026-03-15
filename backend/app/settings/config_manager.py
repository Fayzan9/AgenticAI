"""
ConfigManager: Handles reading and updating configuration values from config.py
"""
import os
import re
from pathlib import Path
from typing import Dict, Any, Optional


class ConfigManager:
    """Manages configuration file reading and updates"""
    
    def __init__(self):
        self.config_path = Path(__file__).resolve().parent.parent.parent / "config.py"
    
    def get_all_configs(self) -> Dict[str, Any]:
        """Read all configuration values from config.py"""
        configs = {}
        
        if not self.config_path.exists():
            return configs
        
        content = self.config_path.read_text()
        
        # Extract simple variable assignments
        patterns = [
            (r'^CORS_ORIGINS\s*=\s*(.+)$', 'CORS_ORIGINS'),
            (r'^CORS_ALLOW_CREDENTIALS\s*=\s*(.+)$', 'CORS_ALLOW_CREDENTIALS'),
            (r'^CORS_ALLOW_METHODS\s*=\s*(.+)$', 'CORS_ALLOW_METHODS'),
            (r'^CORS_ALLOW_HEADERS\s*=\s*(.+)$', 'CORS_ALLOW_HEADERS'),
            (r'^ENABLE_CONTAINER_EXECUTION\s*=\s*(.+)$', 'ENABLE_CONTAINER_EXECUTION'),
        ]
        
        for pattern, key in patterns:
            match = re.search(pattern, content, re.MULTILINE)
            if match:
                value = match.group(1).strip()
                configs[key] = self._parse_value(value)
        
        # Extract multi-line strings (prompts)
        configs['AGENT_PROMPT'] = self._extract_multiline_string(content, 'AGENT_PROMPT')
        configs['RUN_STANDALONE_AGENT_PROMPT'] = self._extract_multiline_string(
            content, 'RUN_STANDALONE_AGENT_PROMPT'
        )
        
        return configs
    
    def update_config(self, key: str, value: Any) -> bool:
        """Update a specific configuration value"""
        if not self.config_path.exists():
            return False
        
        content = self.config_path.read_text()
        
        # Handle multi-line strings (prompts)
        if key in ['AGENT_PROMPT', 'RUN_STANDALONE_AGENT_PROMPT']:
            return self._update_multiline_string(key, value)
        
        # Handle simple assignments
        pattern = rf'^({key}\s*=\s*)(.+)$'
        new_value = self._format_value(value)
        replacement = rf'\1{new_value}'
        
        new_content, count = re.subn(pattern, replacement, content, flags=re.MULTILINE)
        
        if count > 0:
            self.config_path.write_text(new_content)
            return True
        
        return False
    
    def _parse_value(self, value_str: str) -> Any:
        """Parse string representation to Python value"""
        value_str = value_str.strip()
        
        # Handle booleans
        if value_str in ['True', 'False']:
            return value_str == 'True'
        
        # Handle lists
        if value_str.startswith('[') and value_str.endswith(']'):
            return eval(value_str)
        
        # Handle strings
        if value_str.startswith('"') and value_str.endswith('"'):
            return value_str[1:-1]
        if value_str.startswith("'") and value_str.endswith("'"):
            return value_str[1:-1]
        
        # Handle os.getenv calls
        if 'os.getenv' in value_str:
            return value_str
        
        return value_str
    
    def _format_value(self, value: Any) -> str:
        """Format Python value to string representation"""
        if isinstance(value, bool):
            return str(value)
        elif isinstance(value, list):
            return repr(value)
        elif isinstance(value, str):
            # Don't quote os.getenv calls
            if 'os.getenv' in value:
                return value
            return repr(value)
        return str(value)
    
    def _extract_multiline_string(self, content: str, var_name: str) -> Optional[str]:
        """Extract multi-line string variable"""
        pattern = rf'{var_name}\s*=\s*"""(.*?)"""'
        match = re.search(pattern, content, re.DOTALL)
        if match:
            return match.group(1).strip()
        return None
    
    def _update_multiline_string(self, key: str, value: str) -> bool:
        """Update a multi-line string variable"""
        content = self.config_path.read_text()
        pattern = rf'({key}\s*=\s*""").*?(""")'
        replacement = rf'\1\n{value}\n\2'
        
        new_content, count = re.subn(pattern, replacement, content, flags=re.DOTALL)
        
        if count > 0:
            self.config_path.write_text(new_content)
            return True
        
        return False
