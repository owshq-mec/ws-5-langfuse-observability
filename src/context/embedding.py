import asyncio
import os
from collections.abc import Iterable
from functools import cached_property

from fastembed import TextEmbedding
from fastembed.rerank.cross_encoder import TextCrossEncoder
from graphiti_core.cross_encoder.client import CrossEncoderClient
from graphiti_core.embedder.client import EmbedderClient


class LocalEmbedder(EmbedderClient):
    """Runs a small ONNX embedding model on the CPU, so Graphiti needs no embedding API key."""

    def __init__(self, model_name: str):
        self.model_name = model_name

    @cached_property
    def _model(self) -> TextEmbedding:
        return TextEmbedding(model_name=self.model_name, cache_dir=os.environ.get("FASTEMBED_CACHE_PATH"))

    def _embed(self, texts: list[str]) -> list[list[float]]:
        return [vector.tolist() for vector in self._model.embed(texts)]

    async def create(self, input_data: str | list[str] | Iterable[int] | Iterable[Iterable[int]]) -> list[float]:
        text = input_data if isinstance(input_data, str) else next(iter(input_data))
        vectors = await asyncio.to_thread(self._embed, [str(text)])
        return vectors[0]

    async def create_batch(self, input_data_list: list[str]) -> list[list[float]]:
        return await asyncio.to_thread(self._embed, list(input_data_list))


class LocalReranker(CrossEncoderClient):
    """Local cross-encoder reranker, replacing Graphiti's default OpenAI reranker."""

    def __init__(self, model_name: str):
        self.model_name = model_name

    @cached_property
    def _model(self) -> TextCrossEncoder:
        return TextCrossEncoder(model_name=self.model_name, cache_dir=os.environ.get("FASTEMBED_CACHE_PATH"))

    async def rank(self, query: str, passages: list[str]) -> list[tuple[str, float]]:
        if not passages:
            return []
        scores = await asyncio.to_thread(lambda: list(self._model.rerank(query, passages)))
        return sorted(zip(passages, map(float, scores)), key=lambda pair: pair[1], reverse=True)
