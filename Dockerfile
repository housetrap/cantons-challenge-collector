FROM ghcr.io/astral-sh/uv:python3.14-trixie

WORKDIR /app
ENV PYTHONPATH=/app/src

COPY README.md uv.lock pyproject.toml /app/
COPY src/ /app/src/
COPY templates/ /app/templates/
COPY static/ /app/static/
RUN uv sync --frozen --no-install-project

CMD ["sh", "-c", "uv run --no-sync hypercorn cantons_challenge_collector.site:app --insecure-bind [::]:${PORT:-3000}"]
