import logging
import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import dotenv_values

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data" / "orbisa"
STATE_DIR = ROOT / ".helix"


def load_env() -> None:
    # Non-empty .env values win, and empty ones never mask a value exported in the shell.
    for key, value in dotenv_values(os.environ.get("HELIX_ENV_FILE") or ROOT / ".env").items():
        if value:
            os.environ[key] = value
    # An exported-but-empty ANTHROPIC_BASE_URL makes the SDK build URLs with no scheme.
    for key in ("ANTHROPIC_BASE_URL", "ANTHROPIC_AUTH_TOKEN", "ANTHROPIC_API_KEY"):
        if os.environ.get(key) == "":
            del os.environ[key]
    os.environ.setdefault("GRAPHITI_TELEMETRY_ENABLED", "false")
    os.environ.setdefault("EMBEDDING_DIM", "384")
    os.environ.setdefault("SEMAPHORE_LIMIT", "4")
    logging.getLogger("neo4j.notifications").setLevel(logging.ERROR)


load_env()


@dataclass(frozen=True)
class Settings:
    neo4j_uri: str
    neo4j_user: str
    neo4j_password: str
    group_id: str
    ingest_model: str
    agent_model: str
    embedding_model: str
    reranker_model: str
    mcp_host: str
    mcp_port: int

    @property
    def mcp_url(self) -> str:
        return os.environ.get("HELIX_MCP_URL") or f"http://{self.mcp_host}:{self.mcp_port}/mcp"


def settings() -> Settings:
    env = os.environ.get
    return Settings(
        neo4j_uri=env("NEO4J_URI", "bolt://localhost:7687"),
        neo4j_user=env("NEO4J_USER", "neo4j"),
        neo4j_password=env("NEO4J_PASSWORD", "helix-dev-password"),
        group_id=env("HELIX_GROUP_ID", "orbisa"),
        ingest_model=env("HELIX_INGEST_MODEL", "claude-haiku-5-5"),
        agent_model=env("HELIX_AGENT_MODEL", "claude-opus-5-5"),
        embedding_model=env("HELIX_EMBEDDING_MODEL", "BAAI/bge-small-en-v1.5"),
        reranker_model=env("HELIX_RERANKER_MODEL", "Xenova/ms-marco-MiniLM-L-6-v2"),
        mcp_host=env("HELIX_MCP_HOST", "127.0.0.1"),
        mcp_port=int(env("HELIX_MCP_PORT", "8765")),
    )
