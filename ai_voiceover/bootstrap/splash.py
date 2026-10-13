"""Lightweight console splash shown before Qt spins up.

Kept dependency-free so it renders even if PySide6 fails to import.
"""

from __future__ import annotations

import sys
import time

from ai_voiceover import __version__
from ai_voiceover.config.constants import APP_NAME

_BANNER = r"""
   _   ___   __      __   ___  ___ ___ ___  ___ ___
  /_\ |_ _|  \ \    / /__| _ \/ __| __| _ \/ __| __|
 / _ \ | |    \ \/\/ / _ \  _/ (_ | _||   / (__| _|
/_/ \_\___|    \_/\_/\___/_|  \___|___|_|_\\___|___|
"""


def show_splash(duration: float = 0.6) -> None:
    sys.stdout.write(_BANNER)
    sys.stdout.write(f"  {APP_NAME} v{__version__}  ·  voiceover script engine\n\n")
    sys.stdout.flush()
    time.sleep(duration)