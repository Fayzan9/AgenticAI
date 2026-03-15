"""
WorkflowManager: Handles reading and updating workflow template files
"""
from pathlib import Path
from typing import List, Dict, Optional


class WorkflowFile:
    """Represents a workflow file"""
    def __init__(self, name: str, path: Path):
        self.name = name
        self.path = path
        self.content = None
    
    def load_content(self):
        """Load file content"""
        if self.path.exists():
            self.content = self.path.read_text()
    
    def save_content(self, content: str):
        """Save file content"""
        self.path.write_text(content)
        self.content = content
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'name': self.name,
            'content': self.content
        }


class WorkflowManager:
    """Manages workflow template files"""
    
    def __init__(self):
        self.workflow_dir = Path(__file__).resolve().parent.parent.parent / "workflow_templates" / "workflow"
    
    def list_files(self) -> List[str]:
        """List all workflow files"""
        if not self.workflow_dir.exists():
            return []
        
        return [f.name for f in self.workflow_dir.glob("*.md")]
    
    def get_file(self, filename: str) -> Optional[WorkflowFile]:
        """Get a specific workflow file"""
        file_path = self.workflow_dir / filename
        
        if not file_path.exists() or not file_path.suffix == '.md':
            return None
        
        workflow_file = WorkflowFile(filename, file_path)
        workflow_file.load_content()
        
        return workflow_file
    
    def get_all_files(self) -> List[WorkflowFile]:
        """Get all workflow files with content"""
        files = []
        
        for filename in self.list_files():
            workflow_file = self.get_file(filename)
            if workflow_file:
                files.append(workflow_file)
        
        return files
    
    def update_file(self, filename: str, content: str) -> bool:
        """Update a workflow file"""
        file_path = self.workflow_dir / filename
        
        if not file_path.exists() or not file_path.suffix == '.md':
            return False
        
        workflow_file = WorkflowFile(filename, file_path)
        workflow_file.save_content(content)
        
        return True
