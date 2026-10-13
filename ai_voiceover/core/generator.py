"""Script generation engine.

Takes a topic brief, calls the configured LLM client, splits the returned
prose into cues, and hands them to the timing engine. The generator is
synchronous — the Qt layer runs it on a worker thread via QThreadPool.
"""

from __future__ import annotations

import logging
import re

from ai_voiceover.config.prompts import SCRIPT_SYSTEM_PROMPT, SCRIPT_USER_TEMPLATE
from ai_voiceover.models.cue import Cue
from ai_voiceover.models.script import Script, ScriptMeta
from ai_voiceover.services.llm.base import LLMClient
from ai_voiceover.utils.text_cleanup import normalize_for_narration

log = logging.getLogger(__name__)

_SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z<])")


def _estimate_target_words(duration_sec: int, wpm: int) -> int:
    return int((duration_sec / 60.0) * wpm)


def _split_into_cues(prose: str) -> list[str]:
    """Split prose into cue-sized chunks. One sentence per cue, merged if tiny."""
    sentences = [s.strip() for s in _SENTENCE_SPLIT.split(prose) if s.strip()]
    merged: list[str] = []
    buffer = ""
    for s in sentences:
        candidate = f"{buffer} {s}".strip() if buffer else s
        if len(candidate.split()) < 6 and buffer:
            buffer = candidate
        else:
            if buffer:
                merged.append(buffer)
            buffer = s
    if buffer:
        merged.append(buffer)
    return merged


def generate_script(
    topic: str,
    duration_sec: int,
    llm: LLMClient,
    *,
    tone: str = "neutral",
    audience: str = "general",
    wpm: int = 155,
) -> Script:
    """Generate a full script from a topic brief.

    Returns a Script with cues left untimed (all zero-length). Call
    `ai_voiceover.core.timing.apply_timing` to fill start/end offsets.
    """
    target_words = _estimate_target_words(duration_sec, wpm)
    user_prompt = SCRIPT_USER_TEMPLATE.format(
        topic=topic,
        duration_sec=duration_sec,
        tone=tone,
        audience=audience,
        wpm=wpm,
        target_words=target_words,
    )

    log.info("generating script topic=%r target_words=%d", topic, target_words)
    raw = llm.complete(system=SCRIPT_SYSTEM_PROMPT, user=user_prompt)
    cleaned = normalize_for_narration(raw)

    meta = ScriptMeta(
        topic=topic,
        tone=tone,
        audience=audience,
        wpm=wpm,
        provider_llm=getattr(llm, "name", "unknown"),
    )
    script = Script(meta=meta)

    for i, chunk in enumerate(_split_into_cues(cleaned)):
        script.add_cue(Cue(index=i, text=chunk, start_ms=0, end_ms=0))

    script.reindex()
    return script