"""Dispatches a Script to the configured TTS provider.

Handles per-cue synthesis, stitches the audio, and writes a sidecar SRT.
Retries transient provider errors via tenacity.
"""

from __future__ import annotations

import logging
from pathlib import Path

from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from ai_voiceover.models.script import Script
from ai_voiceover.models.voice_profile import VoiceProfile
from ai_voiceover.services.tts.base import TTSService, TTSError
from ai_voiceover.services.export.srt_writer import write_srt

log = logging.getLogger(__name__)


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1.5, min=1, max=12),
    retry=retry_if_exception_type(TTSError),
    reraise=True,
)
def _synth_cue(tts: TTSService, text: str, profile: VoiceProfile) -> bytes:
    return tts.synthesize(text, profile)


def render_script(
    script: Script,
    profile: VoiceProfile,
    tts: TTSService,
    out_dir: Path,
) -> Path:
    """Synthesize every cue, write concatenated audio + SRT sidecar.

    Returns the path to the rendered audio file.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    chunks: list[bytes] = []
    for cue in script.cues:
        log.debug("synthesizing cue %d (%d chars)", cue.index, len(cue.text))
        chunks.append(_synth_cue(tts, cue.text, profile))

    audio_path = out_dir / f"{script.meta.topic[:40].replace(' ', '_') or 'voiceover'}.mp3"
    tts.write_stream(chunks, audio_path)

    srt_path = audio_path.with_suffix(".srt")
    write_srt(script, srt_path)
    log.info("rendered %d cues -> %s", len(script.cues), audio_path)
    return audio_path