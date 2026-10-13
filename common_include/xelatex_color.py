#!/usr/bin/env python3
"""Run a LaTeX engine with colored terminal diagnostics.

All arguments after the engine name are passed to the engine unchanged.

Usage:
    xelatex_color.py <engine> [engine args ...]

Example:
    xelatex_color.py xelatex -file-line-error -halt-on-error \
        -output-format=pdf -interaction=nonstopmode \
        -output-directory=./build main.tex
"""

from __future__ import annotations

import argparse
import logging
import re
import shutil
import subprocess
import sys
from collections.abc import Sequence
from typing import ClassVar, Final


class ColorFormatter(logging.Formatter):
    COLORS: ClassVar[dict[int, str]] = {
        logging.INFO: "\033[32m",        # Green
        logging.WARNING: "\033[33m",     # Yellow
        logging.ERROR: "\033[31m",       # Red
        logging.DEBUG: "\033[90m",       # Gray
        logging.CRITICAL: "\033[1;31m",  # Bold red
    }
    RESET: ClassVar[str] = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        message: str = super().format(record)
        color: str = self.COLORS.get(record.levelno, "")
        return f"{color}{message}{self.RESET}" if color else message


RESET: Final[str] = "\033[0m"
RED: Final[str] = "\033[31m"
YELLOW: Final[str] = "\033[33m"
GREEN: Final[str] = "\033[32m"

INFO_RE: Final[re.Pattern[str]] = re.compile(r"\[INFO\]")
WARN_RE: Final[re.Pattern[str]] = re.compile(r"\[WARN\]")
ERROR_RE: Final[re.Pattern[str]] = re.compile(r"\[ERROR\]")

LATEX_ERROR_RE: Final[re.Pattern[str]] = re.compile(
    r"^!\s|"
    r":\d+:\s*(?:Undefined control sequence|"
    r"LaTeX Error|Package .* Error|"
    r"Missing .* inserted|"
    r"Runaway argument|"
    r"Emergency stop)\b|"
    r"LaTeX Error:|"
    r"Package .* Error:|"
    r"Fatal error|"
    r".*Error:|"
    r"Emergency stop\."
)

LATEX_WARN_RE: Final[re.Pattern[str]] = re.compile(
    r"LaTeX Warning:|"
    r"Package .* Warning:|"
    r"Class .* Warning:|"
    r"Overfull \\[hv]box|"
    r"Underfull \\[hv]box|"
    r"undefined references|"
    r"undefined citations"
)


def colorize(line: str) -> str:
    """Color a complete diagnostic line."""
    if ERROR_RE.search(line) or LATEX_ERROR_RE.search(line):
        return f"{RED}{line}{RESET}"

    if WARN_RE.search(line) or LATEX_WARN_RE.search(line):
        return f"{YELLOW}{line}{RESET}"

    if INFO_RE.search(line):
        return f"{GREEN}{line}{RESET}"

    return line


def build_parser() -> argparse.ArgumentParser:
    """Create the command-line parser."""
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Run a LaTeX engine with colored diagnostic logs.",
        usage="%(prog)s engine [engine_args ...]",
    )
    parser.add_argument(
        "engine",
        help="LaTeX engine, e.g. xelatex, lualatex, pdflatex",
    )
    parser.add_argument(
        "engine_args",
        nargs=argparse.REMAINDER,
        help="Arguments passed to the engine unchanged (options, .tex file, ...)",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    logging.addLevelName(logging.WARNING, "WARN")
    handler: logging.StreamHandler[object] = logging.StreamHandler()
    handler.setFormatter(
        ColorFormatter("%(filename)s:%(lineno)d: [%(levelname)s] %(message)s")
    )

    logging.basicConfig(
        level=logging.INFO,
        handlers=[handler],
        force=True,
    )

    parser: argparse.ArgumentParser = build_parser()
    args: argparse.Namespace = parser.parse_args(argv)

    engine: str = args.engine
    engine_args: list[str] = list(args.engine_args)

    # Allow an optional "--" separator between engine and its arguments.
    if engine_args and engine_args[0] == "--":
        engine_args = engine_args[1:]

    executable: str | None = shutil.which(engine)
    if executable is None:
        logging.error("%s not found; check PATH and TeX installation.", engine)
        return 127

    command: list[str] = [executable, *engine_args]

    logging.info("Running: %s", " ".join(command))

    process: subprocess.Popen[str] | None = None
    return_code: int
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

        if process.stdout is None:
            raise RuntimeError("failed to capture subprocess output")

        line: str
        for line in process.stdout:
            sys.stdout.write(colorize(line))
            sys.stdout.flush()

        return_code = process.wait()

    except KeyboardInterrupt:
        logging.warning("Interrupted by user.")
        if process is not None and process.poll() is None:
            process.terminate()
            process.wait()
        return 130

    if return_code == 0:
        logging.info("%s finished successfully.", engine)
    else:
        logging.error("%s exited with code %s.", engine, return_code)

    return return_code


if __name__ == "__main__":
    raise SystemExit(main())
