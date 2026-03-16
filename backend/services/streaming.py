"""
streaming.py: Streaming/event logic for CodexCLI
"""

import json
import logging
import os
from typing import Optional, Tuple
from datetime import datetime

from services.codex_cli import CodexCLI
from config import WORKFLOW_DIR, ACTIVE_MODEL

logger = logging.getLogger(__name__)


# ---------------------------------------------------------
# SSE utilities
# ---------------------------------------------------------

def _sse(data: dict) -> str:
    """Format a Server-Sent Event payload."""
    return f"data: {json.dumps(data)}\n\n"


# ---------------------------------------------------------
# Event parsing
# ---------------------------------------------------------

def _parse_codex_event(line: str) -> Optional[dict]:
    """Parse a JSON line from Codex output."""
    try:
        return json.loads(line)
    except json.JSONDecodeError:
        return None


def _extract_thinking(event: dict) -> Optional[dict]:
    """
    Extract thinking log events from Codex event JSON.
    Returns thinking log object or None.
    """

    item = event.get("item", {})
    event_type = event.get("type")
    item_type = item.get("type")

    if event_type == "item.started" and item_type == "command_execution":
        command = item.get("command")
        if command:
            return {"type": "started", "command": command}

    if event_type == "item.completed" and item_type == "command_execution":
        command = item.get("command")
        output = (item.get("aggregated_output") or "").strip()

        snippet = output.replace("\n", " ")[:120]

        if command:
            return {
                "type": "completed",
                "command": command,
                "output": snippet,
            }

    return None


def _extract_assistant_message(event: dict) -> Optional[str]:
    """Extract final assistant message from event."""
    if (
        event.get("type") == "item.completed"
        and event.get("item", {}).get("type") == "agent_message"
    ):
        return event.get("item", {}).get("text")

    return None


def _extract_usage(event: dict) -> Optional[dict]:
    """Extract token usage from turn.completed event."""
    if event.get("type") == "turn.completed":
        return event.get("usage")
    return None


# ---------------------------------------------------------
# Thread persistence
# ---------------------------------------------------------

def _save_assistant_message(thread_id: str, text: str, thinking_logs: list):
    """Persist assistant response to thread service."""

    try:
        from app.threads.threads import add_message_to_thread_service

        add_message_to_thread_service(
            thread_id=thread_id,
            role="assistant",
            text=text,
            thinking_logs=thinking_logs,
        )

        logger.info("Saved assistant response to thread %s", thread_id)

    except Exception:
        logger.exception("Failed to persist assistant response to thread")


# ---------------------------------------------------------
# Streaming generator
# ---------------------------------------------------------

def stream_codex_events(prompt: str, thread_id: Optional[str] = None):
    """
    Generator yielding SSE events from Codex `exec --json`.
    """

    logger.info("Starting Codex event stream")

    cli = CodexCLI(cwd=WORKFLOW_DIR, model=ACTIVE_MODEL)

    event_count = 0
    assistant_final_response: str = ""
    thinking_logs: list = []

    try:
        print(f'(stream_codex_events) PROMPT LOADED SUCCESSFULLY: {prompt[:500]}...')  # Debug log to confirm prompt loading  
        
        for stream, line in cli.run_streaming(prompt, yield_lines=True):

            # returncode event
            if stream == "returncode":
                logger.info("Codex execution completed with code %s", line)
                yield _sse({"type": "returncode", "code": line})
                break

            event_count += 1

            # -------------------------------------------------
            # Parse Codex JSON events
            # -------------------------------------------------

            if thread_id and stream == "stdout":

                event_data = _parse_codex_event(line)

                if event_data:

                    # assistant response
                    text = _extract_assistant_message(event_data)
                    if text:
                        assistant_final_response = text

                    # thinking logs
                    thinking = _extract_thinking(event_data)
                    if thinking:
                        thinking_logs.append(thinking)
                        logger.info("[THINKING] %s", thinking)

            # forward event to SSE
            if stream == "stdout":
                logger.info("STDOUT: %s", line[:200] if len(line) > 200 else line)
            elif stream == "stderr":
                logger.warning("STDERR: %s", line)
            
            yield _sse({"stream": stream, "line": line})

        logger.info("Streaming completed. Total events: %s", event_count)

        # -------------------------------------------------
        # Save assistant response to thread
        # -------------------------------------------------

        if thread_id and assistant_final_response:
            _save_assistant_message(
                thread_id,
                assistant_final_response,
                thinking_logs,
            )

    except Exception as e:

        logger.exception("Error during streaming")

        yield _sse({
            "type": "error",
            "message": str(e),
        })


# ---------------------------------------------------------
# Streaming with execution tracking
# ---------------------------------------------------------

def stream_codex_events_with_tracking(
    prompt: str, 
    agent_name: str,
    execution_id: str,
    thread_id: Optional[str] = None
):
    """
    Generator yielding SSE events from Codex `exec --json` with execution tracking.
    Saves all logs to execution history.
    """
    from app.agent_executions.service import add_execution_log, complete_execution
    from app.agent_executions.models import ExecutionLog

    logger.info(f"Starting Codex event stream with tracking for execution {execution_id}")

    cli = CodexCLI(cwd=WORKFLOW_DIR, model=ACTIVE_MODEL)

    event_count = 0
    assistant_final_response: str = ""
    thinking_logs: list = []
    usage_data = None

    try:
        
        for stream, line in cli.run_streaming(prompt, yield_lines=True):

            # returncode event
            if stream == "returncode":
                logger.info("Codex execution completed with code %s", line)
                complete_execution(agent_name, execution_id, line, usage_data)
                
                # Log completion
                add_execution_log(
                    agent_name,
                    execution_id,
                    ExecutionLog(
                        timestamp=datetime.now().isoformat(),
                        type="status",
                        content=f"Execution completed with code {line}",
                        details={"return_code": line}
                    )
                )
                
                yield _sse({"type": "returncode", "code": line})
                break

            event_count += 1

            # -------------------------------------------------
            # Parse Codex JSON events and track them
            # -------------------------------------------------

            if stream == "stdout":
                event_data = _parse_codex_event(line)

                if event_data:
                    # Extract usage data
                    usage = _extract_usage(event_data)
                    if usage:
                        usage_data = usage
                        logger.info("Captured token usage: %s", usage)
                    
                    # assistant response
                    text = _extract_assistant_message(event_data)
                    if text:
                        assistant_final_response = text
                        add_execution_log(
                            agent_name,
                            execution_id,
                            ExecutionLog(
                                timestamp=datetime.now().isoformat(),
                                type="message",
                                content=text,
                                details={"message_type": "assistant"}
                            )
                        )

                    # thinking logs for command execution
                    thinking = _extract_thinking(event_data)
                    if thinking:
                        thinking_logs.append(thinking)
                        logger.info("[THINKING] %s", thinking)
                        
                        # Track command execution
                        if thinking["type"] == "started":
                            add_execution_log(
                                agent_name,
                                execution_id,
                                ExecutionLog(
                                    timestamp=datetime.now().isoformat(),
                                    type="command_start",
                                    content=thinking["command"],
                                    details=thinking
                                )
                            )
                        elif thinking["type"] == "completed":
                            add_execution_log(
                                agent_name,
                                execution_id,
                                ExecutionLog(
                                    timestamp=datetime.now().isoformat(),
                                    type="command_complete",
                                    content=thinking["command"],
                                    details=thinking
                                )
                            )

            # forward event to SSE
            if stream == "stdout":
                logger.debug("STDOUT: %s", line[:200] if len(line) > 200 else line)
            elif stream == "stderr":
                logger.warning("STDERR: %s", line)
            
        # -------------------------------------------------
        # Save assistant response to thread if provided
        # -------------------------------------------------

        if thread_id and assistant_final_response:
            _save_assistant_message(
                thread_id,
                assistant_final_response,
                thinking_logs,
            )

    except Exception as e:

        logger.exception("Error during streaming")
        
        # Mark execution as failed
        complete_execution(agent_name, execution_id, -1, None)
        add_execution_log(
            agent_name,
            execution_id,
            ExecutionLog(
                timestamp=datetime.now().isoformat(),
                type="status",
                content=f"Execution failed: {str(e)}",
                details={"error": str(e)}
            )
        )

        yield _sse({
            "type": "error",
            "message": str(e),
        })