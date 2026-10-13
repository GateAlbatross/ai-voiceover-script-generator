"""Application-wide constants. No logic here — just numbers and strings."""

from __future__ import annotations

APP_NAME = "AI Voiceover Script Generator"
ORG_NAME = "VoiceLab"
APP_ID = "ai-voiceover-script-generator"

MIN_PYTHON = (3, 11)

# Script engine limits
MAX_SCRIPT_CHARS = 250_000
MAX_CUES = 4_000
MIN_CUE_MS = 350
MAX_CUE_MS = 18_000
DEFAULT_WPM = 155

# Timing
DEFAULT_LEAD_IN_MS = 200
DEFAULT_TAIL_MS = 400

# Providers
LLM_PROVIDERS = ("openai", "anthropic", "ollama", "lmstudio")
TTS_PROVIDERS = ("elevenlabs", "azure", "piper", "system_sapi")

# Paths (relative to user config dir)
SETTINGS_FILENAME = "app_settings.json"
LOG_DIRNAME = "logs"
CACHE_DIRNAME = "cache"