# Outreach Multi-Agent Refactor

This version consolidates the duplicated application architectures into shared agents, services, clients, domain state, utilities and thin Lambda adapters.

## Main flow
`main.py/app.py -> orchestrator -> agent -> service -> client -> external API`

## Consolidated areas
- Microsoft Graph authentication/calendar operations are shared.
- Teams authentication/message delivery is shared.
- Response and logging utilities are shared.
- LinkedIn client operations are shared.
- Posting generation and publishing are separated.
- Lambda handlers are thin deployment adapters.
- Runtime logs, credentials, Python executables and caches are excluded from Git.

## Important
The original ingestion pipeline was preserved as DynamoDB + OpenAI embeddings because that is what the uploaded source code implements. No database/vector-store semantics were invented during this refactor.

The original project also contained broken imports and legacy references (for example the old Lambda import paths in `main.py` and the old comment pipeline stage imports). Those were removed from the new application path.
