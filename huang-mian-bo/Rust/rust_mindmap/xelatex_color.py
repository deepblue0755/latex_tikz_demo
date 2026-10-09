#!/usr/bin/env python3
"""Run XeLaTeX with colored terminal diagnostics."""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
from collections.abc import Sequence

RESET = "\033[0m"
RED = "\033[31m"
YELLOW = "\033[33m"
GREEN = "\033[32m"

INFO_RE = re.compile(r"\bBUILD:INFO:")
WARN_RE = re.compile(r"\bBUILD:WARN:")
ERROR_RE = re.compile(r"\bBUILD:ERROR:")

LATEX_ERROR_RE = re.compile(
    r"^!\s|"
    r":\d+:\s*(?:Undefined control sequence|"
    r"LaTeX Error|Package .* Error|"
    r"Missing .* inserted|"
    r"Runaway argument|"
    r"Emergency stop)\b|"
    r"LaTeX Error:|"
    r"Package .* Error:|"
    r"Emergency stop\."
)

LATEX_WARN_RE = re.compile(
    r"LaTeX Warning:|"
    r"Package .* Warning:|"
    r"Class .* Warning:|"
    r"Overfull \\[hv]box|"
    r"Underfull \\[hv]box|"
    r"undefined references|"
    r"undefined citations"
)


def supports_color(mode: str) -> bool:
    """Determine whether ANSI color should be enabled."""
    if mode == "always":
        return True
    if mode == "never":
        return False

    return sys.stdout.isatty() and "NO_COLOR" not in os.environ


def colorize(line: str, enabled: bool) -> str:
    """Color a complete diagnostic line."""
    if not enabled:
        return line

    if ERROR_RE.search(line) or LATEX_ERROR_RE.search(line):
        return f"{RED}{line}{RESET}"

    if WARN_RE.search(line) or LATEX_WARN_RE.search(line):
        return f"{YELLOW}{line}{RESET}"

    if INFO_RE.search(line):
        return f"{GREEN}{line}{RESET}"

    return line


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Compile a LaTeX document with colored XeLaTeX logs."
    )
    parser.add_argument("source", help="Main .tex file")
    parser.add_argument(
        "--color",
        choices=("auto", "always", "never"),
        default="auto",
        help="Color policy (default: auto)",
    )

    args, extra_args = parser.parse_known_args(argv)

    executable = shutil.which("xelatex")
    if executable is None:
        print(
            "[ERROR] xelatex not found; check PATH and TeX installation.",
            file=sys.stderr,
        )
        return 127

    command = [
        executable,
        "-file-line-error",
        "-halt-on-error",
        "-interaction=nonstopmode",
        "-output-directory=./build",
        *extra_args,
        args.source,
    ]

    enabled = supports_color(args.color)

    print(f"[INFO] Running: {' '.join(command)}", flush=True)

    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            bufsize=1,
        )

        assert process.stdout is not None

        for line in process.stdout:
            sys.stdout.write(colorize(line, enabled))
            sys.stdout.flush()

        return_code = process.wait()

    except KeyboardInterrupt:
        print("\n[WARN] Interrupted by user.", flush=True)
        if "process" in locals() and process.poll() is None:
            process.terminate()
            process.wait()
        return 130

    if return_code == 0:
        print(f"{GREEN}[INFO] XeLaTeX finished successfully.{RESET}"
              if enabled else
              "[INFO] XeLaTeX finished successfully.")
    else:
        print(f"{RED}[ERROR] XeLaTeX exited with code "
              f"{return_code}.{RESET}"
              if enabled else
              f"[ERROR] XeLaTeX exited with code {return_code}.")

    return return_code


if __name__ == "__main__":
    raise SystemExit(main())
