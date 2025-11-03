# ---- Stage 1: Builder - Compile the Rust Wheel ----
FROM rust:1.91.0-slim AS builder

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y python3 build-essential && \
    rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/

WORKDIR /app

COPY pyproject.toml Cargo.toml Cargo.lock* ./
COPY src ./src

RUN uv venv /opt/venv && \
    PATH="/opt/venv/bin:$PATH" && \
    uv pip install maturin && \
    maturin build --release --strip -o /wheels --find-interpreter


# ---- Stage 2: Final Production Image ----
FROM python:3.14-slim

ENV PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN groupadd --system app && useradd --system --gid app app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/

RUN uv venv $VIRTUAL_ENV

WORKDIR /app

COPY --from=builder /wheels /wheels
COPY server.py .

RUN uv pip install --no-cache-dir /wheels/*.whl && \
    rm -rf /wheels && \
    chown -R app:app /app /opt/venv

USER app

EXPOSE $PORT

CMD ["uv", "run", "--no-cache", "server.py"]
