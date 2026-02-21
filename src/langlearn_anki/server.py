from __future__ import annotations

from pathlib import Path

from langlearn_types import DeckRequest
from mcp.server.fastmcp import FastMCP

from langlearn_anki import __version__
from langlearn_anki.ankigen import (
    build_deck as build_deck_impl,
    load_media_manifest,
    result_to_dict,
)

mcp = FastMCP("langlearn-anki")
mcp._mcp_server.version = __version__  # pyright: ignore[reportPrivateUsage]


@mcp.tool()
def ping() -> str:
    "Health check tool."
    return "ok"


@mcp.tool()
def build_deck(
    language: str,
    deck: str,
    data_dir: str,
    output_path: str | None = None,
    media_json: str | None = None,
) -> str:
    "Build an Anki deck from cards.json and provided media assets."
    data_path = Path(data_dir)
    media = load_media_manifest(Path(media_json), data_path) if media_json else None
    request = DeckRequest(
        language=language,
        deck=deck,
        data_dir=data_path,
        media=media,
        output_path=Path(output_path) if output_path else None,
    )
    result = build_deck_impl(request)
    return str(result_to_dict(result))


def run_server() -> None:
    "Run the MCP server."
    mcp.run()
