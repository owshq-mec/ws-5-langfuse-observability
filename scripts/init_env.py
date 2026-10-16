"""Create .env from .env.example and fill every empty secret with a random value.

Safe to re-run: existing non-empty values are never changed.
    uv run python scripts/init_env.py
"""

import secrets
import shutil
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENV, EXAMPLE = ROOT / ".env", ROOT / ".env.example"

GENERATORS = {
    "POSTGRES_PASSWORD": lambda: secrets.token_urlsafe(18),
    "CLICKHOUSE_PASSWORD": lambda: secrets.token_urlsafe(18),
    "REDIS_AUTH": lambda: secrets.token_urlsafe(18),
    "MINIO_ROOT_PASSWORD": lambda: secrets.token_urlsafe(18),
    "NEXTAUTH_SECRET": lambda: secrets.token_urlsafe(32),
    "SALT": lambda: secrets.token_urlsafe(32),
    "ENCRYPTION_KEY": lambda: secrets.token_hex(32),
    "LANGFUSE_PUBLIC_KEY": lambda: f"pk-lf-{uuid.uuid4()}",
    "LANGFUSE_SECRET_KEY": lambda: f"sk-lf-{uuid.uuid4()}",
    "LANGFUSE_INIT_USER_PASSWORD": lambda: secrets.token_urlsafe(12),
}


def main() -> None:
    if not ENV.exists():
        shutil.copy(EXAMPLE, ENV)
        print("created .env from .env.example")
    lines = ENV.read_text().splitlines()
    present = {line.split("=", 1)[0]: i for i, line in enumerate(lines) if "=" in line and not line.startswith("#")}
    filled = []
    for key, make in GENERATORS.items():
        if key in present:
            i = present[key]
            if lines[i].split("=", 1)[1].strip():
                continue
            lines[i] = f"{key}={make()}"
        else:
            lines.append(f"{key}={make()}")
        filled.append(key)
    ENV.write_text("\n".join(lines) + "\n")
    print(f"filled: {', '.join(filled) or 'nothing (all set)'}")
    values = dict(line.split("=", 1) for line in ENV.read_text().splitlines() if "=" in line and not line.startswith("#"))
    if not values.get("ANTHROPIC_API_KEY"):
        print("WARNING: ANTHROPIC_API_KEY is empty in .env")
    print(f"Langfuse UI: http://localhost:3000  user: {values.get('LANGFUSE_INIT_USER_EMAIL', 'engineer@orbisa.example')}  "
          f"password: see LANGFUSE_INIT_USER_PASSWORD in .env")


if __name__ == "__main__":
    main()
