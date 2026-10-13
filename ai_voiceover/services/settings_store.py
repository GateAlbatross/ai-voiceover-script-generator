"""Persistent application settings.

Stored as JSON next to the user config dir. API keys are pulled from the
OS keyring when available; the JSON only holds a boolean "has_key" flag.
"""

from __future__ import annotations

import json
import logging
from dataclasses import asdict, dataclass, field
from pathlib import Path

from ai_voiceover.config.constants import SETTINGS_FILENAME

log = logging.getLogger(__name__)

try:
    import keyring  # type: ignore
    _HAS_KEYRING = True
except ImportError:  # pragma: no cover — optional dep
    _HAS_KEYRING = False


@dataclass
class Settings:
    llm_provider: str = "openai"
    tts_provider: str = "elevenlabs"
    default_wpm: int = 155
    default_tone: str = "neutral"
    output_dir: str = ""
    theme: str = "dark"
    recent_topics: list[str] = field(default_factory=list)
    has_api_key: dict[str, bool] = field(default_factory=dict)


class SettingsStore:
    @staticmethod
    def _path() -> Path:
        base = Path.home() / ".ai_voiceover"
        base.mkdir(parents=True, exist_ok=True)
        return base / SETTINGS_FILENAME

    @classmethod
    def load(cls) -> Settings:
        path = cls._path()
        if not path.exists():
            return Settings()
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
            return Settings(**{k: v for k, v in raw.items() if k in Settings.__dataclass_fields__})
        except (json.JSONDecodeError, TypeError) as exc:
            log.warning("settings file corrupt (%s), using defaults", exc)
            return Settings()

    @classmethod
    def save(cls, settings: Settings) -> None:
        cls._path().write_text(json.dumps(asdict(settings), indent=2), encoding="utf-8")

    @staticmethod
    def get_api_key(provider: str) -> str | None:
        if not _HAS_KEYRING:
            return None
        try:
            return keyring.get_password("ai-voiceover-script-generator", provider)
        except Exception:  # noqa: BLE001 — keyring backends vary wildly
            log.warning("keyring read failed for %s", provider)
            return None

    @staticmethod
    def set_api_key(provider: str, key: str) -> None:
        if _HAS_KEYRING:
            keyring.set_password("ai-voiceover-script-generator", provider, key)