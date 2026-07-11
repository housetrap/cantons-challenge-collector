dev:
    uv run  hypercorn --reload --log-level debug cantons_challenge_collector.site:app

up:
    docker compose -f docker/dev/compose.yaml up -d
