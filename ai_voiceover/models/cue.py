"""A single timed voiceover cue."""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator

from ai_voiceover.config.constants import MIN_CUE_MS, MAX_CUE_MS


class Cue(BaseModel):
    """One line of narration with start/end timing in milliseconds."""

    index: int = Field(ge=0)
    text: str
    start_ms: int = Field(ge=0)
    end_ms: int = Field(ge=0)
    speaker: str | None = None
    emphasis_words: list[str] = Field(default_factory=list)
    pause_after_ms: int = 0

    @field_validator("text")
    @classmethod
    def _non_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("cue text must not be empty")
        return v

    @field_validator("end_ms")
    @classmethod
    def _end_after_start(cls, v: int, info) -> int:
        start = info.data.get("start_ms", 0)
        if v <= start:
            raise ValueError("end_ms must be greater than start_ms")
        return v

    @property
    def duration_ms(self) -> int:
        return self.end_ms - self.start_ms

    def clamped(self) -> "Cue":
        """Return a copy with duration clamped to sane bounds."""
        dur = max(MIN_CUE_MS, min(MAX_CUE_MS, self.duration_ms))
        return self.model_copy(update={"end_ms": self.start_ms + dur})