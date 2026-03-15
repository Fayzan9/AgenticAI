"""
streaming.py: Streaming/event logic for CodexCLI
"""
import json
import logging
from typing import Optional
from services.codex_cli import CodexCLI
from config import AGENT_CWD

logger = logging.getLogger(__name__)

def stream_codex_events(prompt: str, thread_id: Optional[str] = None):
    """Generator that yields SSE events from Codex exec --json."""
    logger.info("Starting Codex event stream")
    cli = CodexCLI(cwd=AGENT_CWD)
    event_count = 0
    assistant_final_response = ""
    thinking_logs = []  # List[dict]

    try:
        for event in cli.run_streaming(prompt, yield_lines=True):
            event_count += 1
            if event[0] == "returncode":
                logger.info(f"Codex execution completed with return code: {event[1]}")
                yield f"data: {json.dumps({'type': 'returncode', 'code': event[1]})}\n\n"
            else:
                stream, line = event

                # If thread_id is provided, collect final assistant response and thinking logs
                if thread_id and stream == "stdout":
                    try:
                        event_data = json.loads(line)
                        if (
                            event_data.get("type") == "item.completed"
                            and event_data.get("item", {}).get("type") == "agent_message"
                        ):
                            text = event_data.get("item", {}).get("text", "")
                            if text:
                                assistant_final_response = text
                        elif (
                            event_data.get("type") == "item.started"
                            and event_data.get("item", {}).get("type") == "command_execution"
                        ):
                            command = event_data.get("item", {}).get("command", "")
                            if command:
                                log_obj = {"type": "started", "command": command}
                                thinking_logs.append(log_obj)
                                logger.info(f"[THINKING] {log_obj}")
                        elif (
                            event_data.get("type") == "item.completed"
                            and event_data.get("item", {}).get("type") == "command_execution"
                        ):
                            command = event_data.get("item", {}).get("command", "")
                            output = (event_data.get("item", {}).get("aggregated_output", "") or "").strip()
                            snippet = output.replace("\n", " ")[:120]
                            if command:
                                log_obj = {"type": "completed", "command": command, "output": snippet}
                                thinking_logs.append(log_obj)
                                logger.info(f"[THINKING] {log_obj}")
                    except (json.JSONDecodeError, KeyError):
                        pass

                yield f"data: {json.dumps({'stream': stream, 'line': line})}\n\n"

        logger.info(f"Streaming completed. Total events: {event_count}")

        # Save assistant response to thread if thread_id provided
        if thread_id and assistant_final_response:
            logger.info(f"Saving assistant response to thread {thread_id}")
            try:
                from services.thread_storage import get_thread_storage
                storage = get_thread_storage()
                storage.add_message_to_thread(
                    thread_id,
                    "assistant",
                    assistant_final_response,
                    thinking_logs=thinking_logs,
                )
                logger.info(f"Successfully saved assistant response to thread {thread_id}")
            except Exception as e:
                logger.error(f"Error saving assistant response to thread: {str(e)}", exc_info=True)

    except Exception as e:
        logger.error(f"Error during streaming: {str(e)}", exc_info=True)
        yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"
