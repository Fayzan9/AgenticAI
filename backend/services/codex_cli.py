"""
CodexCLI: Wrapper for the Codex CLI to run prompts and chat non-interactively.
Refactored for clearer structure and maintainability.
"""

import json
import shutil
import subprocess
import sys
import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterator, Optional, Union

from config import THREADS_DIR, ACCESS_TO_INTERNET


# ------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------

@dataclass
class CodexConfig:
    cwd: Path
    model: Optional[str] = None
    sandbox: Optional[str] = None
    full_auto: bool = False
    json_events: bool = True
    skip_git_repo_check: bool = True
    codex_bin: Optional[str] = None

    def resolve_bin(self) -> str:
        return self.codex_bin or shutil.which("codex") or "codex"


# ------------------------------------------------------------------
# Command Builder
# ------------------------------------------------------------------

class CodexCommandBuilder:

    def __init__(self, config: CodexConfig):
        self.config = config

    def build(self, prompt: Optional[str] = None) -> list[str]:
        cfg = self.config
        args = [cfg.resolve_bin()]
        
        # Global flags before subcommand
        if ACCESS_TO_INTERNET:
            args.append("--search")
        
        # Add exec subcommand
        args.append("exec")

        if cfg.json_events:
            args.append("--json")

        if cfg.skip_git_repo_check:
            args.append("--skip-git-repo-check")

        if cfg.model:
            args += ["-m", cfg.model]

        if cfg.sandbox:
            args += ["-s", cfg.sandbox]

        if cfg.full_auto:
            args.append("--full-auto")

        args += [
            "-C",
            str(cfg.cwd),
            "--add-dir",
            str(THREADS_DIR.resolve()),
        ]

        if prompt:
            args.append(prompt)

        return args


# ------------------------------------------------------------------
# Process Runner
# ------------------------------------------------------------------

class CodexRunner:

    def __init__(self, cwd: Path):
        self.cwd = cwd

    def run(
        self,
        args: list[str],
        *,
        timeout: Optional[float] = None,
        env: Optional[dict[str, str]] = None,
        capture: bool = True,
    ) -> subprocess.CompletedProcess:

        return subprocess.run(
            args,
            cwd=str(self.cwd),
            capture_output=capture,
            text=True,
            timeout=timeout,
            env=env,
        )

    def popen(
        self,
        args: list[str],
        *,
        env: Optional[dict[str, str]] = None,
    ) -> subprocess.Popen:

        return subprocess.Popen(
            args,
            cwd=str(self.cwd),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env,
        )


# ------------------------------------------------------------------
# Public API
# ------------------------------------------------------------------

class CodexCLI:

    def __init__(
        self,
        *,
        cwd: Optional[str | Path] = None,
        model: Optional[str] = None,
        sandbox: Optional[str] = None,
        full_auto: bool = False,
        json_events: bool = True,
        skip_git_repo_check: bool = True,
        codex_bin: Optional[str] = None,
    ):

        cwd_path = Path(cwd).resolve() if cwd else Path.cwd()

        self.config = CodexConfig(
            cwd=cwd_path,
            model=model,
            sandbox=sandbox,
            full_auto=full_auto,
            json_events=json_events,
            skip_git_repo_check=skip_git_repo_check,
            codex_bin=codex_bin,
        )

        self.builder = CodexCommandBuilder(self.config)
        self.runner = CodexRunner(self.config.cwd)

    # ------------------------------------------------------------------

    def run(self, prompt: str, *, timeout=None, env=None):
        args = self.builder.build(prompt)
        return self.runner.run(args, timeout=timeout, env=env)

    # ------------------------------------------------------------------

    def run_live(self, prompt: str, *, timeout=None, env=None) -> int:
        args = self.builder.build(prompt)

        proc = subprocess.run(
            args,
            cwd=str(self.config.cwd),
            stdout=None,
            stderr=None,
            text=True,
            timeout=timeout,
            env=env,
        )

        return proc.returncode

    # ------------------------------------------------------------------

    def run_async(self, prompt: str, *, env=None) -> subprocess.Popen:
        args = self.builder.build(prompt)
        return self.runner.popen(args, env=env)

    # ------------------------------------------------------------------

    def run_streaming(
        self,
        prompt: str,
        *,
        timeout=None,
        env=None,
        yield_lines: bool = False,
    ):
        args = self.builder.build(prompt)

        proc = subprocess.Popen(
            args,
            cwd=str(self.config.cwd),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            env=env,
        )

        if yield_lines:

            import queue

            q = queue.Queue()

            def read_stdout():
                for line in proc.stdout:
                    q.put(("stdout", line.rstrip("\n")))
                q.put(("stdout_end", None))

            def read_stderr():
                for line in proc.stderr:
                    q.put(("stderr", line.rstrip("\n")))
                q.put(("stderr_end", None))

            threading.Thread(target=read_stdout, daemon=True).start()
            threading.Thread(target=read_stderr, daemon=True).start()

            def generator():
                ended = 0

                while ended < 2:
                    stream, line = q.get()

                    if stream.endswith("_end"):
                        ended += 1
                        continue

                    yield (stream, line)

                proc.wait()
                yield ("returncode", proc.returncode)

            return generator()

        # fallback: non-yield streaming
        return self.run_live(prompt, timeout=timeout, env=env)

    # ------------------------------------------------------------------

    def chat(self, prompt: str, *, timeout=None, collect_json_events=False):

        result = self.run(prompt, timeout=timeout)

        output = {
            "ok": result.returncode == 0,
            "returncode": result.returncode,
            "stdout": result.stdout or "",
            "stderr": result.stderr or "",
            "events": [],
        }

        if self.config.json_events and collect_json_events and result.stdout:

            for line in result.stdout.splitlines():
                try:
                    output["events"].append(json.loads(line))
                except json.JSONDecodeError:
                    continue

        return output

    # ------------------------------------------------------------------

    def exec(
        self,
        prompt: str,
        *,
        output_last_message_path: Optional[str | Path] = None,
        timeout=None,
        env=None,
    ):

        args = self.builder.build(prompt)

        if output_last_message_path:
            args += ["-o", str(output_last_message_path)]

        return self.runner.run(args, timeout=timeout, env=env)