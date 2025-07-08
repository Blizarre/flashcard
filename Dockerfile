FROM ghcr.io/astral-sh/uv:debian-slim

WORKDIR /app

ADD uv.lock pyproject.toml /app

RUN uv sync --locked

ADD main.py /app
ADD static/ /app/static/
ADD data/ /app/data/

CMD ["uv", "run", "uvicorn", "--host", "0.0.0.0", "main:app"]
