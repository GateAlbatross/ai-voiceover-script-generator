"""Application entry point.

Checks Python version, verifies bundled ffmpeg, initializes the settings
store, then hands control to the Qt application. Exits with code 2 on
missing runtime dependencies so installers can detect the failure.
"""

from __future__ import annotations

import sys
import shutil
from pathlib import Path

from ai_voiceover.bootstrap.splash import show_splash
from ai_voiceover.config.constants import MIN_PYTHON, APP_NAME
from ai_voiceover.utils.logging_setup import configure_logging


def _check_python() -> None:
    if sys.version_info < MIN_PYTHON:
        sys.stderr.write(
            f"{APP_NAME} requires Python {MIN_PYTHON[0]}.{MIN_PYTHON[1]}+ "
            f"(found {sys.version.split()[0]})\n"
        )
        raise SystemExit(2)


def _check_ffmpeg() -> Path:
    found = shutil.which("ffmpeg")
    if found is None:
        sys.stderr.write(
            "ffmpeg not found on PATH. Install ffmpeg or set VO_FFMPEG_PATH.\n"
        )
        raise SystemExit(2)
    return Path(found)


def main(argv: list[str] | None = None) -> int:
    _check_python()
    configure_logging()
    _check_ffmpeg()
    show_splash()

    from ai_voiceover.handlers.app_window import launch  # deferred: Qt import cost

    return launch(argv if argv is not None else sys.argv[1:])


if __name__ == "__main__":
    raise SystemExit(main())