FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:0.9 /uv /usr/local/bin/uv

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    FASTEMBED_CACHE_PATH=/opt/fastembed \
    PATH=/opt/venv/bin:$PATH \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml uv.lock README.md ./
RUN uv sync --frozen --no-dev --no-install-project

COPY src ./src
RUN uv sync --frozen --no-dev

# Bake the local embedding and reranker models into the image, so containers start offline.
RUN python -c "from context.config import settings; from fastembed import TextEmbedding; from fastembed.rerank.cross_encoder import TextCrossEncoder; s = settings(); TextEmbedding(s.embedding_model, cache_dir='/opt/fastembed'); TextCrossEncoder(s.reranker_model, cache_dir='/opt/fastembed')"

COPY data ./data

EXPOSE 8765
CMD ["python", "-m", "context.mcp"]
