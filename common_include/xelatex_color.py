#!/usr/bin/env python3
"""Run XeLaTeX with colored terminal diagnostics."""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import logging
from collections.abc import Sequence

class ColorFormatter(logging.Formatter):
    COLORS = {
        logging.INFO: "\033[32m",      # Green
        logging.WARNING: "\033[33m",   # Yellow
        logging.ERROR: "\033[31m",     # Red
        logging.DEBUG: "\033[90m",     # Gray
        logging.CRITICAL: "\033[1;31m",  # Bold red
    }
    RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        message = super().format(record)

        # Redirected output should not contain ANSI escape codes.
        if not sys.stderr.isatty():
            return message

        color = self.COLORS.get(record.levelno, "")
        return f"{color}{message}{self.RESET}" if color else message

RESET = "\033[0m"
RED = "\033[31m"
YELLOW = "\033[33m"
GREEN = "\033[32m"

INFO_RE = re.compile(r"\[INFO\]")
WARN_RE = re.compile(r"\[WARN\]")
ERROR_RE = re.compile(r"\[ERROR\]")

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
    logging.addLevelName(logging.WARNING, "WARN")
    handler = logging.StreamHandler()
    handler.setFormatter(
        ColorFormatter(
            "%(filename)s:%(lineno)d: [%(levelname)s] %(message)s"
        )
    )

    logging.basicConfig(
        level=logging.INFO,
        handlers=[handler],
        force=True,
    )

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
        logging.info("XeLaTeX finished successfully.")
    else:
        logging.error("XeLaTeX exited with code %s.",return_code)

    return return_code


if __name__ == "__main__":
    raise SystemExit(main())
