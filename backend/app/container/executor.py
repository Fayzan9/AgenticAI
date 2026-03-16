"""
Simple container executor for agent runs.
Spawn → Execute → Exit pattern with pre-built images.
"""

import logging
import os
import subprocess
from pathlib import Path
from typing import Iterator, Optional

from .container_configuration import (
    CONTAINER_IMAGE,
    CPU_LIMIT,
    MEMORY_LIMIT,
    EXECUTION_TIMEOUT,
    ENABLE_ROOTLESS,
    ENABLE_NETWORK,
    PODMAN_BIN,
)
from config import WORKFLOW_DIR, EXECUTIONS_DIR, AGENT_DIR

logger = logging.getLogger(__name__)


class ContainerExecutionError(Exception):
    """Raised when container execution fails."""
    pass


class ContainerExecutor:
    """
    Simple executor for running agents in containers.
    
    Flow:
    1. Spawn container with volumes mounted
    2. Container executes agent and writes output
    3. Container exits automatically (--rm)
    """
    
    def __init__(self, image: Optional[str] = None):
        """
        Initialize executor.
        
        Args:
            image: Container image name (default from config)
        """
        self.image = image or CONTAINER_IMAGE
        self.podman_bin = PODMAN_BIN
        
    def execute_agent(
        self, 
        agent_name: str, 
        execution_id: str, 
        user_prompt: str
    ) -> Iterator[str]:
        """
        Execute agent in container and stream output.
        
        Args:
            agent_name: Name of the agent to execute
            execution_id: Unique execution identifier
            user_prompt: User's input prompt
            
        Yields:
            Lines of output from the container (JSON events)
            
        Raises:
            ContainerExecutionError: If container fails to start or execute
        """
        cmd = self._build_command(agent_name, execution_id, user_prompt)
        
        # Log command (mask API key for security)
        cmd_log = [arg if 'OPENAI_API_KEY=' not in arg else 'OPENAI_API_KEY=***' for arg in cmd]
        logger.info(f"Podman command: {' '.join(cmd_log[:15])}...")
        
        logger.info(
            f"Starting container execution: agent={agent_name}, "
            f"execution_id={execution_id}"
        )
        
        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=str(WORKFLOW_DIR),  # Set working directory for container execution
            )
            
            # Stream stdout line by line
            if process.stdout:
                for line in iter(process.stdout.readline, ''):
                    if line:
                        yield line.rstrip()
            
            # Wait for completion
            return_code = process.wait(timeout=EXECUTION_TIMEOUT)
            
            if return_code != 0:
                stderr = process.stderr.read() if process.stderr else ""
                logger.error(
                    f"Container execution failed: return_code={return_code}, "
                    f"stderr={stderr}"
                )
                raise ContainerExecutionError(
                    f"Container exited with code {return_code}: {stderr}"
                )
            
            logger.info(
                f"Container execution completed: agent={agent_name}, "
                f"execution_id={execution_id}"
            )
            
        except subprocess.TimeoutExpired:
            logger.error(f"Container execution timeout: execution_id={execution_id}")
            process.kill()
            raise ContainerExecutionError(
                f"Execution timeout after {EXECUTION_TIMEOUT}s"
            )
        except Exception as e:
            logger.exception(f"Container execution error: {e}")
            raise ContainerExecutionError(f"Execution failed: {e}")
    
    def execute_agent_sync(
        self, 
        agent_name: str, 
        execution_id: str, 
        user_prompt: str
    ) -> int:
        """
        Execute agent in container synchronously (wait for completion).
        
        Args:
            agent_name: Name of the agent to execute
            execution_id: Unique execution identifier
            user_prompt: User's input prompt
            
        Returns:
            Return code (0 for success)
            
        Raises:
            ContainerExecutionError: If container fails
        """
        cmd = self._build_command(agent_name, execution_id, user_prompt)
        
        # Log command (mask API key for security)
        cmd_log = [arg if 'OPENAI_API_KEY=' not in arg else 'OPENAI_API_KEY=***' for arg in cmd]
        logger.info(f"Podman command: {' '.join(cmd_log[:15])}...")
        
        logger.info(
            f"Starting sync container execution: agent={agent_name}, "
            f"execution_id={execution_id}"
        )
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=EXECUTION_TIMEOUT,
                cwd=str(WORKFLOW_DIR)  # Set working directory for container execution,
            )
            
            if result.returncode != 0:
                logger.error(
                    f"Container execution failed: return_code={result.returncode}, "
                    f"stderr={result.stderr}"
                )
                raise ContainerExecutionError(
                    f"Container exited with code {result.returncode}: {result.stderr}"
                )
            
            logger.info(
                f"Container execution completed: agent={agent_name}, "
                f"execution_id={execution_id}"
            )
            
            return result.returncode
            
        except subprocess.TimeoutExpired:
            logger.error(f"Container execution timeout: execution_id={execution_id}")
            raise ContainerExecutionError(
                f"Execution timeout after {EXECUTION_TIMEOUT}s"
            )
        except Exception as e:
            logger.exception(f"Container execution error: {e}")
            raise ContainerExecutionError(f"Execution failed: {e}")
    
    def _build_command(
        self, 
        agent_name: str, 
        execution_id: str, 
        user_prompt: str
    ) -> list[str]:
        """
        Build podman command for agent execution.
        
        Args:
            agent_name: Name of the agent
            execution_id: Execution identifier
            user_prompt: User prompt
            
        Returns:
            Command as list of strings
        """
        # Resolve paths
        executions_dir = EXECUTIONS_DIR
        
        # Get API key from environment
        api_key = os.getenv('OPENAI_API_KEY', '')
        if api_key:
            # Mask for logging (show first 7 chars: sk-proj-)
            masked_key = api_key[:10] + '...' if len(api_key) > 10 else '***'
            logger.info(f"OPENAI_API_KEY found on host: {masked_key}")
        else:
            logger.warning("OPENAI_API_KEY not found in host environment!")
        
        logger.info(f"Container network: {'ENABLED' if ENABLE_NETWORK else 'DISABLED'}")
        
        cmd = [
            self.podman_bin,
            "run",
            "--rm",  # Auto-remove container after exit
            "--privileged",  # Required for proper file access in Podman on macOS
            
            # Resource limits
            f"--cpus={CPU_LIMIT}",
            f"--memory={MEMORY_LIMIT}",
            
            # Volumes (read-only agents, read-write executions)
            "-v", f"{WORKFLOW_DIR.resolve()}:/workspace/workflow:ro",
            "-v", f"{executions_dir.resolve()}:/workspace/executions:rw",
        ]
        
        # Mount codex auth credentials if they exist on host
        codex_auth = Path.home() / ".codex" / "auth.json"
        if codex_auth.exists():
            logger.info(f"Mounting codex auth credentials from {codex_auth}")
            # Mount entire .codex directory to preserve config structure
            cmd.extend(["-v", f"{Path.home() / '.codex'}:/root/.codex:ro"])
        else:
            logger.warning(f"Codex auth.json not found at {codex_auth}. Run 'codex login' on host first.")
        
        cmd.extend([
            # Environment variables
            "-e", f"AGENT_NAME={agent_name}",
            "-e", f"EXECUTION_ID={execution_id}",
            "-e", f"USER_PROMPT={user_prompt}",
            "-e", f"OPENAI_API_KEY={api_key}",
            
            # Security
            "--security-opt", "no-new-privileges",
        ])
        
        # Network isolation (disable network by default)
        if not ENABLE_NETWORK:
            cmd.append("--network=none")
        
        # Podman on macOS/rootless: no userns needed
        # The default behavior should work fine
        
        # Image
        cmd.append(self.image)
        
        return cmd
    
    def check_image_exists(self) -> bool:
        """
        Check if the container image exists locally.
        
        Returns:
            True if image exists, False otherwise
        """
        try:
            result = subprocess.run(
                [self.podman_bin, "image", "exists", self.image],
                capture_output=True,
                timeout=10,
            )
            return result.returncode == 0
        except Exception as e:
            logger.warning(f"Failed to check image existence: {e}")
            return False
    
    def pull_image(self) -> None:
        """
        Pull the container image from registry.
        
        Raises:
            ContainerExecutionError: If pull fails
        """
        logger.info(f"Pulling container image: {self.image}")
        
        try:
            result = subprocess.run(
                [self.podman_bin, "pull", self.image],
                capture_output=True,
                text=True,
                timeout=300,  # 5 min timeout for pull
            )
            
            if result.returncode != 0:
                raise ContainerExecutionError(
                    f"Failed to pull image: {result.stderr}"
                )
            
            logger.info(f"Successfully pulled image: {self.image}")
            
        except subprocess.TimeoutExpired:
            raise ContainerExecutionError("Image pull timeout")
        except Exception as e:
            raise ContainerExecutionError(f"Failed to pull image: {e}")
