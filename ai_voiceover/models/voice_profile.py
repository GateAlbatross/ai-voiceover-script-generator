"""A reusable voice configuration for TTS dispatch."""

from __future__ import annotations

from pydantic import BaseModel, Field


class VoiceProfile(BaseModel):
    name: str
    provider: str
    voice_id: str
    language: str = "en-US"
    stability: float = Field(default=0.5, ge=0.0, le=1.0)
    similarity: float = Field(default=0.75, ge=0.0, le=1.0)
    style_exaggeration: float = Field(default=0.0, ge=0.0, le=1.0)
    speaking_rate: float = Field(default=1.0, ge=0.5, le=2.0)
    pitch_semitones: float = Field(default=0.0, ge=-12.0, le=12.0)
    notes: str = ""

    def to_tts_payload(self) -> dict[str, object]:
        return {
            "voice_id": self.voice_id,
            "language": self.language,
            "stability": self.stability,
            "similarity": self.similarity,
            "style": self.style_exaggeration,
            "rate": self.speaking_rate,
            "pitch": self.pitch_semitones,
        }