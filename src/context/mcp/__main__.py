"""Run the Helix MCP server over streamable HTTP.

    uv run python -m context.mcp        # serves http://127.0.0.1:8765/mcp by default
"""

from context.config import settings
from context.mcp.server import mcp


def main() -> None:
    s = settings()
    print(f"Helix MCP server on {s.mcp_url}")
    mcp.run(transport="streamable-http", host=s.mcp_host, port=s.mcp_port, streamable_http_path="/mcp")


if __name__ == "__main__":
    main()
