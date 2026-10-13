"""QThread worker wrapping the synchronous generation pipeline."""

from __future__ import annotations

import logging

from PySide6.QtCore import QThread, Signal

from ai_voiceover.config.provider_registry import load_llm
from ai_voiceover.core.generator import generate_script
from ai_voiceover.core.timing import apply_timing
from ai_voiceover.models.script import Script
from ai_voiceover.services.settings_store import SettingsStore

log = logging.getLogger(__name__)


class GenerationWorker(QThread):
    finished_ok = Signal(Script)
    failed = Signal(str)

    def __init__(self, brief: dict) -> None:
        super().__init__()
        self._brief = brief

    def run(self) -> None:  # noqa: D401 — Qt override
        try:
            settings = SettingsStore.load()
            llm = load_llm(settings.llm_provider)
            script = generate_script(
                topic=self._brief["topic"],
                duration_sec=int(self._brief["duration_sec"]),
                llm=llm,
                tone=self._brief.get("tone", "neutral"),
                audience=self._brief.get("audience", "general"),
                wpm=int(self._brief.get("wpm", 155)),
            )
            apply_timing(script)
            self.finished_ok.emit(script)
        except Exception as exc:  # noqa: BLE001 — surface any failure to UI
            log.exception("generation failed")
            self.failed.emit(str(exc))