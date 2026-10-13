# Security Policy

## Supported versions

| Version | Supported          |
|---------|--------------------|
| 0.9.x   | :white_check_mark: |
| 0.8.x   | :white_check_mark: |
| < 0.8   | :x:                |

## Reporting a vulnerability

Please do **not** open a public issue for security problems. Email
`security@voicelab.dev` with:

- A description of the issue
- Steps to reproduce
- Affected version(s)
- Any proof-of-concept code (please keep it minimal)

We aim to acknowledge within 72 hours and ship a patch within 14 days for
confirmed high-severity issues.

## Scope

In scope:

- Arbitrary code execution via crafted `.voscript` project files
- Path traversal in the SRT/VTT export writers
- Injection into subprocess calls to bundled `ffmpeg`
- Credential leakage from `services/llm/` when logging is verbose

Out of scope:

- Issues requiring local admin already
- Denial of service from absurdly large scripts (we cap at 250k chars)
- Self-XSS in the debug console

## API key handling

API keys are stored in the OS keyring via `keyring` when available, falling
back to an obfuscated local file. We never transmit keys anywhere except the
provider endpoint the user configured. Logs redact anything matching the
known key prefixes for supported providers.