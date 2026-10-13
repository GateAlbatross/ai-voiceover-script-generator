"""OpenAI chat-completions client.

Uses httpx directly to avoid the SDK's telemetry. Reads the API key from