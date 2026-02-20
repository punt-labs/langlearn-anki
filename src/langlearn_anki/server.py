from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from langlearn_anki import __version__

mcp = FastMCP("langlearn-anki")
mcp._mcp_server.version = __version__  # pyright: ignore[reportPrivateUsage]


@mcp.tool()
def ping() -> str:
    "Health check tool."
    return "ok"


def run_server() -> None:
    "Run the MCP server."
    mcp.run()
