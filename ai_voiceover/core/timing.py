"""Timing engine: assigns start/end offsets to cues.

Two modes:
  - `estimate`: word-count based, fast, no audio needed.
  - `forced_align`: after TTS synthesis, uses provider word timings.
"""

from __future__ import annotations

import logging

from ai_voiceover.config.constants import (
    DEFAULT_LEAD_IN_MS,
    DEFAULT_TAIL_MS,
    MIN_CUE_MS,
)
from ai_voiceover.models.script import Script

log = logging.getLogger(__name__)

_MS_PER_WORD_AT_155WPM = 60_000 / 155


def _ms_for_text(text: str, wpm: int) -> int:
    words = max(1, len(text.split()))
    ms_per_word = 60_000 / wpm
    return int(words * ms_per_word)


def apply_timing(script: Script, *, lead_in_ms: int = DEFAULT_LEAD_IN_MS,
                 tail_ms: int = DEFAULT_TAIL_MS) -> Script:
    """Estimate cue timings from word counts. Mutates script in place."""
    cursor = lead_in_ms
    for cue in script.cues:
        dur = max(MIN_CUE_MS, _ms_for_text(cue.text, script.meta.wpm))
        cue.start_ms = cursor
        cue.end_ms = cursor + dur
        cursor = cue.end_ms + cue.pause_after_ms
    if script.cues:
        script.cues[-1].end_ms += tail_ms
    log.debug("applied timing to %d cues, total=%dms",
              len(script.cues), script.total_duration_ms)
    return script


def apply_forced_alignment(script: Script, word_timings: list[tuple[str, int, int]]) -> Script:
    """Overwrite cue timings using provider word-level timings.

    `word_timings` is a flat list of (word, start_ms, end_ms) in reading order.
    Cues are matched greedily by word count against the original text.
    """
    cursor = 0
    for cue in script.cues:
        cue_words = len(cue.text.split())
        slice_ = word_timings[cursor:cursor + cue_words]
        if not slice_:
            break
        cue.start_ms = slice_[0][1]
        cue.end_ms = slice_[-1][2]
        cursor += cue_words
    return script