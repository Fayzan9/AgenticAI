"""
Minimal Codex CLI wrapper focused on streaming.
"""

import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, Optional, Tuple

from config import THREADS_DIR, ACCESS_TO_INTERNET


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# Command builder
# ---------------------------------------------------------

class CodexCommandBuilder:

    def __init__(self, config: CodexConfig):
        self.config = config

    def build(self, prompt: Optional[str] = None) -> list[str]:
        cfg = self.config

        args = [cfg.resolve_bin()]

        if ACCESS_TO_INTERNET:
            args.append("--search")

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


# ---------------------------------------------------------
# CLI wrapper
# ---------------------------------------------------------

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

    # ---------------------------------------------------------

    def run_streaming(
        self,
        prompt: str,
        *,
        env: Optional[dict] = None,
    ) -> Iterator[Tuple[str, str]]:

        args = self.builder.build(prompt)

        proc = subprocess.Popen(
            args,
            cwd=str(self.config.cwd),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            env=env,
        )

        for line in proc.stdout:
            yield ("stdout", line.rstrip("\n"))

        proc.wait()
        yield ("returncode", proc.returncode)