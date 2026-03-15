"""
streaming.py: Streaming/event logic for CodexCLI
"""
import json
from services.codex_cli import CodexCLI

def stream_codex_events(prompt: str):
    """Generator that yields SSE events from Codex exec --json."""
    cli = CodexCLI()
    for event in cli.run_streaming(prompt, yield_lines=True):
        if event[0] == "returncode":
            yield f"data: {json.dumps({'type': 'returncode', 'code': event[1]})}\n\n"
        else:
            stream, line = event
            yield f"data: {json.dumps({'stream': stream, 'line': line})}\n\n"
