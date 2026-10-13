"""Registry mapping provider names to adapter classes.

Adapters are imported lazily so the app boots even when an optional SDK
isn't installed — the provider just shows as unavailable in the UI.
"""

from __future__ import annotations

from importlib import import_module
from typing import Callable

from ai_voiceover.services.tts.base import TTSService
from ai_voiceover.services.llm.base import LLMClient

_TTS_PATHS: dict[str, str] = {
    "elevenlabs": "ai_voiceover.services.tts.elevenlabs_adapter:ElevenLabsAdapter",
    "azure": "ai_voiceover.services.tts.azure_adapter:AzureTTSAdapter",
    "piper": "ai_voiceover.services.tts.piper_adapter:PiperAdapter",
    "system_sapi": "ai_voiceover.services.tts.sapi_adapter:SapiAdapter",
}

_LLM_PATHS: dict[str, str] = {
    "openai": "ai_voiceover.services.llm.openai_client:OpenAIClient",
    "anthropic": "ai_voiceover.services.llm.anthropic_client:AnthropicClient",
    "ollama": "ai_voiceover.services.llm.ollama_client:OllamaClient",
    "lmstudio": "ai_voiceover.services.llm.lmstudio_client:LMStudioClient",
}


def _resolve(path: str) -> Callable[[], object]:
    module_name, _, attr = path.partition(":")

    def factory() -> object:
        return getattr(import_module(module_name), attr)()

    return factory


def load_tts(provider: str) -> TTSService:
    if provider not in _TTS_PATHS:
        raise KeyError(f"unknown TTS provider: {provider!r}")
    return _resolve(_TTS_PATHS[provider])()  # type: ignore[return-value]


def load_llm(provider: str) -> LLMClient:
    if provider not in _LLM_PATHS:
        raise KeyError(f"unknown LLM provider: {provider!r}")
    return _resolve(_LLM_PATHS[provider])()  # type: ignore[return-value]


def available_tts() -> list[str]:
    return list(_TTS_PATHS.keys())


def available_llm() -> list[str]:
    return list(_LLM_PATHS.keys())