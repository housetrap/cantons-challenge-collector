dev:
    uv run  hypercorn --reload --log-level debug cantons_challenge_collector.site:app

up:
    docker compose -f docker/dev/compose.yaml up

upd:
    docker compose -f docker/dev/compose.yaml up -d

down:
    docker compose -f docker/dev/compose.yaml down

build-docker:
    docker compose -f docker/dev/compose.yaml build
