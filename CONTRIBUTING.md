# Contributing to ai-voiceover-script-generator

First off — thanks for wanting to help. This project exists because a handful
of voiceover nerds got tired of writing SRT-timed scripts by hand. If you've
ever stared at a 12-minute explainer video and thought "I should script this,"
you're our people.

## Ground rules

- Be decent. Critique code, not people.
- One feature per PR. If you're touching the TTS adapter layer AND the SRT
  timing engine, split it.
- Every new provider adapter needs a test in `tests/`.
- No PR that bumps the LLM prompt templates without a before/after sample
  committed under `docs/samples/` (open a draft PR if you don't have a
  sample yet).

## Dev setup

```bash
git clone https://github.com/voicelab/ai-voiceover-script-generator
cd ai-voiceover-script-generator
python -m venv .venv
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
pip install -r requirements-dev.txt
python -m ai_voiceover.app --dev
```

The app is a PySide6 desktop tool. On first launch it writes
`app_settings.json` next to the executable (gitignored). Delete it to reset.

## Project layout

- `ai_voiceover/` — package root
  - `bootstrap/` — entry point, splash, dependency checks
  - `core/` — engine: script generation, timing, TTS dispatch
  - `handlers/` — Qt signal handlers, menu actions, drag-drop
  - `services/` — LLM clients, TTS adapters, export writers
  - `models/` — dataclasses for Script, Cue, VoiceProfile
  - `utils/` — text cleanup, SSML helpers, time formatting
  - `config/` — constants, prompt templates, provider registry

## Adding a TTS provider

1. Create `ai_voiceover/services/tts/<provider>_adapter.py`.
2. Subclass `TTSService` from `ai_voiceover/services/tts/base.py`.
3. Register in `ai_voiceover/config/provider_registry.py`.
4. Add a smoke test in `tests/test_tts_adapters.py`.

## Style

- Black, line length 100.
- Ruff clean. `ruff check ai_voiceover`.
- Type hints on every public function. `mypy ai_voiceover` should pass.
- No bare `except:`. Catch specific exceptions.

## Commit messages

Conventional-ish. `feat(tts): add ElevenLabs v3 adapter`. `fix(srt): clamp
cue end before next cue start`. Not strict, but keep it readable.

## Reporting issues

Use the issue template. Include: OS build, Python version, provider being
used, and a redacted copy of `logs/ai_voiceover.log` if the crash is on
generation.