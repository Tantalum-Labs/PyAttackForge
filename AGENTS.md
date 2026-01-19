# AGENTS

Success command: ./ci.sh

Rules:
- Make minimal changes; no unrelated refactors.
- Always rerun ./ci.sh after modifications.
- Tests must clean up docker containers on failure.
- Prefer docs in docs/attackforge/ssapi/index.md and docs/attackforge/ssapi/markdown/*
- Treat live integration tests as the source of truth if docs conflict.
- Never guess URL slugs; use the local manifest.json or fetch from the live API.
