import os

from graphiti_core import Graphiti
from graphiti_core.llm_client import LLMConfig
from graphiti_core.llm_client.anthropic_client import AnthropicClient

from context.config import settings
from context.embedding import LocalEmbedder, LocalReranker


def build_graphiti() -> Graphiti:
    s = settings()
    llm = AnthropicClient(config=LLMConfig(
        api_key=os.environ.get("ANTHROPIC_API_KEY") or None,
        model=s.ingest_model,
        small_model=s.ingest_model,
    ))
    return Graphiti(
        s.neo4j_uri,
        s.neo4j_user,
        s.neo4j_password,
        llm_client=llm,
        embedder=LocalEmbedder(s.embedding_model),
        cross_encoder=LocalReranker(s.reranker_model),
    )
