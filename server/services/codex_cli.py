"""
CodexCLI: Wrapper for the Codex CLI to run prompts and chat non-interactively.
Moved from codex.py for modularity.
"""

import json
import subprocess
import shutil
import sys
import threading
from pathlib import Path
from typing import Callable, Iterator, Optional, Union

class CodexCLI:
    # ...existing code from codex.py...
    def __init__(self, *, cwd: Optional[str | Path] = None, model: Optional[str] = None, sandbox: Optional[str] = None, full_auto: bool = False, json_events: bool = True, skip_git_repo_check: bool = True, codex_bin: Optional[str] = None):
        self.cwd = Path(cwd).resolve() if cwd else Path.cwd()
        self.model = model
        self.sandbox = sandbox
        self.full_auto = full_auto
        self.json_events = json_events
        self.skip_git_repo_check = skip_git_repo_check
        self._codex_bin = codex_bin or shutil.which("codex") or "codex"

    def _build_args(self, prompt: Optional[str] = None) -> list[str]:
        args = [self._codex_bin, "exec"]
        if self.json_events:
            args.append("--json")
        if self.skip_git_repo_check:
            args.append("--skip-git-repo-check")
        if self.model:
            args.extend(["-m", self.model])
        if self.sandbox:
            args.extend(["-s", self.sandbox])
        if self.full_auto:
            args.append("--full-auto")
        args.extend(["-C", str(self.cwd)])
        if prompt is not None and prompt:
            args.append(prompt)
        return args

    def run(self, prompt: str, *, timeout: Optional[float] = None, env: Optional[dict[str, str]] = None) -> subprocess.CompletedProcess:
        args = self._build_args(prompt=prompt)
        return subprocess.run(
            args,
            cwd=str(self.cwd),
            capture_output=True,
            text=True,
            timeout=timeout,
            env=env,
        )

    def run_live(self, prompt: str, *, timeout: Optional[float] = None, env: Optional[dict[str, str]] = None) -> int:
        args = self._build_args(prompt=prompt)
        proc = subprocess.run(
            args,
            cwd=str(self.cwd),
            stdout=None,  # inherit – print to terminal
            stderr=None,
            text=True,
            timeout=timeout,
            env=env,
        )
        return proc.returncode

    def run_streaming(self, prompt: str, *, timeout: Optional[float] = None, env: Optional[dict[str, str]] = None, on_stdout: Optional[Callable[[str], None]] = None, on_stderr: Optional[Callable[[str], None]] = None, yield_lines: bool = False) -> Union[subprocess.CompletedProcess, Iterator[tuple[str, Union[str, int]]]]:
        args = self._build_args(prompt=prompt)
        proc = subprocess.Popen(
            args,
            cwd=str(self.cwd),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            env=env,
        )

        def read_stdout():
            for line in proc.stdout:
                if on_stdout:
                    on_stdout(line.rstrip("\n"))
                else:
                    print(line, end="", file=sys.stdout)
                    sys.stdout.flush()

        def read_stderr():
            for line in proc.stderr:
                if on_stderr:
                    on_stderr(line.rstrip("\n"))
                else:
                    print(line, end="", file=sys.stderr)
                    sys.stderr.flush()

        if yield_lines:
            def gen():
                import queue
                q = queue.Queue()

                def out_worker():
                    for line in proc.stdout:
                        q.put(("stdout", line.rstrip("\n")))
                    q.put(None)

                def err_worker():
                    for line in proc.stderr:
                        q.put(("stderr", line.rstrip("\n")))
                    q.put(None)

                threading.Thread(target=out_worker, daemon=True).start()
                threading.Thread(target=err_worker, daemon=True).start()
                ended = 0
                while ended < 2:
                    item = q.get()
                    if item is None:
                        ended += 1
                        continue
                    yield item
                proc.wait()
                yield ("returncode", proc.returncode)

            return gen()

        t_out = threading.Thread(target=read_stdout, daemon=True)
        t_err = threading.Thread(target=read_stderr, daemon=True)
        t_out.start()
        t_err.start()
        t_out.join()
        t_err.join()
        proc.wait()
        return subprocess.CompletedProcess(
            args=args, returncode=proc.returncode, stdout=None, stderr=None
        )

    def run_with_stdin(self, prompt: str, *, timeout: Optional[float] = None, env: Optional[dict[str, str]] = None) -> subprocess.CompletedProcess:
        return self.run(prompt, timeout=timeout, env=env)

    def run_async(self, prompt: str, *, timeout: Optional[float] = None, env: Optional[dict[str, str]] = None) -> subprocess.Popen:
        args = self._build_args(prompt=prompt)
        return subprocess.Popen(
            args,
            cwd=str(self.cwd),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env,
        )

    def chat(self, prompt: str, *, timeout: Optional[float] = None, collect_json_events: bool = False) -> dict:
        result = self.run(prompt, timeout=timeout)
        out = {
            "ok": result.returncode == 0,
            "returncode": result.returncode,
            "stdout": result.stdout or "",
            "stderr": result.stderr or "",
            "last_message": "",
            "events": [],
        }
        if self.json_events and result.stdout and collect_json_events:
            events = []
            for line in result.stdout.strip().splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    events.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
            out["events"] = events
        return out

    def exec(self, prompt: str, *, output_last_message_path: Optional[str | Path] = None, timeout: Optional[float] = None, env: Optional[dict[str, str]] = None) -> subprocess.CompletedProcess:
        args = self._build_args(prompt=prompt)
        if output_last_message_path is not None:
            args.extend(["-o", str(output_last_message_path)])
        return subprocess.run(
            args,
            cwd=str(self.cwd),
            capture_output=True,
            text=True,
            timeout=timeout,
            env=env,
        )
