"""The full script document: cues, metadata, and export helpers."""

from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, Field

from ai_voiceover.models.cue import Cue
from ai_voiceover.config.constants import MAX_CUES


class ScriptMeta(BaseModel):
    topic: str
    tone: str = "neutral"
    audience: str = "general"
    wpm: int = 155
    created_at: datetime = Field(default_factory=datetime.utcnow)
    provider_llm: str | None = None
    provider_tts: str | None = None


class Script(BaseModel):
    meta: ScriptMeta
    cues: list[Cue] = Field(default_factory=list)

    def add_cue(self, cue: Cue) -> None:
        if len(self.cues) >= MAX_CUES:
            raise ValueError(f"script exceeds {MAX_CUES} cues")
        self.cues.append(cue)

    @property
    def total_words(self) -> int:
        return sum(len(c.text.split()) for c in self.cues)

    @property
    def total_duration_ms(self) -> int:
        if not self.cues:
            return 0
        return self.cues[-1].end_ms - self.cues[0].start_ms

    def reindex(self) -> None:
        for i, cue in enumerate(self.cues):
            cue.index = i