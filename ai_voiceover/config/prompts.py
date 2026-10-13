"""Prompt templates for the script generation LLM calls.

Kept as module-level strings so prompt diffs show up cleanly in review.
Any change here should be accompanied by a sample under docs/samples/.
"""

from __future__ import annotations

SCRIPT_SYSTEM_PROMPT = """\
You are a senior voiceover scriptwriter. You write for the ear, not the eye.
Rules:
- Short sentences. Vary rhythm. Never stack three clauses with commas.
- Numbers and acronyms written how a narrator would say them.
- No stage directions unless the user asks for them.
- Mark emphasis with <em>...</em> only when a word genuinely needs a push.
- Mark pauses with <break time="Xms"/> where a beat is required.
"""

SCRIPT_USER_TEMPLATE = """\
Topic: {topic}
Target duration: {duration_sec} seconds
Tone: {tone}
Audience: {audience}
Reading pace: {wpm} words per minute

Produce the voiceover script as plain text. Approximate length:
{target_words} words. Do not include a title or intro line.
"""

CONTINUE_TEMPLATE = """\
The script is currently {current_words} words and needs about
{remaining_words} more to hit the target duration. Continue from the last
line without repeating it. Match the established tone.
"""

REWRITE_CUE_TEMPLATE = """\
Rewrite the following voiceover line to be {instruction}. Keep it under
{max_words} words. Return only the rewritten line.

Original: {line}
"""