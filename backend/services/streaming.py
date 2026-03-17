"""
Simple SSE streaming wrapper for Codex CLI with optional execution tracking.
Returns raw output exactly as received with minimal processing.
"""

import json
import logging
from typing import Optional
from datetime import datetime

from services.codex_cli import CodexCLI
from config import WORKFLOW_DIR, ACTIVE_MODEL

logger = logging.getLogger(__name__)


# ---------------------------------------------------------
# SSE helper
# ---------------------------------------------------------

def _sse(data: dict) -> str:
    return f"data: {json.dumps(data)}\n\n"


# ---------------------------------------------------------
# Usage extraction (only helper we need)
# ---------------------------------------------------------

def _extract_usage(line: str) -> Optional[dict]:
    """Extract token usage from turn.completed event."""
    try:
        event = json.loads(line)
        if event.get("type") == "turn.completed":
            return event.get("usage")
    except json.JSONDecodeError:
        pass
    return None


# ---------------------------------------------------------
# Helper to extract assistant message
# ---------------------------------------------------------

def _extract_assistant_message(line: str) -> Optional[str]:
    """Extract final assistant message from item.completed event."""
    try:
        event = json.loads(line)
        if (
            event.get("type") == "item.completed"
            and event.get("item", {}).get("type") == "agent_message"
        ):
            return event.get("item", {}).get("text")
    except json.JSONDecodeError:
        pass
    return None


# ---------------------------------------------------------
# Unified streaming function
# ---------------------------------------------------------

def stream_codex(
    prompt: str,
    thread_id: Optional[str] = None,
    agent_name: Optional[str] = None,
    execution_id: Optional[str] = None,
):
    """
    Unified streaming generator for both chat and agent runs.
    
    Forwards everything from Codex CLI as-is.
    
    Args:
        prompt: The prompt to send to Codex
        thread_id: If provided, saves assistant message to thread (for chat)
        agent_name: Agent/chat identifier for execution tracking
        execution_id: If provided, enables execution tracking and logging
    
    Features:
        - Always: Stream events, extract usage stats
        - If thread_id: Save assistant message with thinking logs to thread
        - If execution_id: Log all output to execution history for debugging
    """

    cli = CodexCLI(
        cwd=WORKFLOW_DIR,
        model=ACTIVE_MODEL,
    )

    # Tracking variables
    assistant_message = ""
    thinking_logs = []
    usage_data = None
    
    # Check if execution tracking is enabled (whenever execution_id is provided)
    track_execution = bool(execution_id and agent_name)
    
    if track_execution:
        logger.info(f"Starting Codex stream with execution tracking for {execution_id}")

    try:

        for stream, line in cli.run_streaming(prompt):

            # Handle return code
            if stream == "returncode":
                
                # Save assistant message to thread if thread_id provided
                if thread_id and assistant_message:
                    try:
                        from app.threads.threads import add_message_to_thread_service
                        
                        add_message_to_thread_service(
                            thread_id=thread_id,
                            role="assistant",
                            text=assistant_message,
                            thinking_logs=thinking_logs,
                        )
                        logger.info(f"Saved assistant message to thread {thread_id}")
                    except Exception as save_error:
                        logger.exception(f"Failed to save assistant message to thread: {save_error}")
                
                # Complete execution tracking if enabled
                if track_execution:
                    from app.agent_executions.service import complete_execution
                    logger.info(f"Codex execution completed with code {line}")
                    complete_execution(agent_name, execution_id, line, usage_data)

                yield _sse({
                    "type": "returncode",
                    "code": line,
                })
                break

            # Extract usage stats (always)
            if stream == "stdout":
                usage = _extract_usage(line)
                if usage:
                    usage_data = usage
                    logger.info("Captured token usage: %s", usage)
            
            # Extract assistant message and collect thinking logs for thread
            if stream == "stdout" and thread_id:
                msg = _extract_assistant_message(line)
                if msg:
                    assistant_message = msg
                
                # Save simplified thinking log (just the raw event)
                try:
                    event = json.loads(line)
                    thinking_logs.append({
                        "type": event.get("type", "unknown"),
                        "data": line[:500]  # Keep first 500 chars of raw event
                    })
                except json.JSONDecodeError:
                    pass
            
            # Log to execution history if tracking enabled
            if track_execution:
                from app.agent_executions.service import add_execution_log
                from app.agent_executions.models import ExecutionLog
                
                add_execution_log(
                    agent_name,
                    execution_id,
                    ExecutionLog(
                        timestamp=datetime.now().isoformat(),
                        type="output",
                        content=line,
                        details={"stream": stream}
                    )
                )

            # Forward to frontend (always)
            yield _sse({
                "stream": stream,
                "data": line,
            })

    except Exception as e:

        logger.exception("Streaming error")
        
        # Mark execution as failed if tracking enabled
        if track_execution:
            from app.agent_executions.service import add_execution_log, complete_execution
            from app.agent_executions.models import ExecutionLog
            
            complete_execution(agent_name, execution_id, -1, None)
            add_execution_log(
                agent_name,
                execution_id,
                ExecutionLog(
                    timestamp=datetime.now().isoformat(),
                    type="error",
                    content=f"Execution failed: {str(e)}",
                    details={"error": str(e)}
                )
            )

        yield _sse({
            "type": "error",
            "message": str(e),
        })