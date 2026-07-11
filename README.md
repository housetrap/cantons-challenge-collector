# Cantons-Challenge API

Minimal FastAPI app with a small Typer CLI and Redis backend.

## Requirements

- Python 3.12+
- uv
- Redis (local or container)

## Run locally

1. Start Redis:

```bash
docker run --rm -p 6379:6379 redis:7-alpine
```

2. Install dependencies:

```bash
uv sync
```

3. Start the API:

```bash
uv run uvicorn --app-dir src cantons_challenge.api:app --reload
```

Open Swagger at http://127.0.0.1:8000/docs

## CLI

Run the CLI entrypoint:

```bash
uv run ac-admin --help
```

## Docker

Build and run:

```bash
docker build -f docker/Dockerfile -t apero-code:local .
docker run --rm -p 8000:8000 apero-code:local
```

## Quality checks

Run all checks with pre-commit:

```bash
uv run --with pre-commit --with pyright pre-commit run --all-files
```
