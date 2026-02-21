from __future__ import annotations

import json
from collections.abc import Mapping
from pathlib import Path

import typer
from langlearn_types import DeckRequest

from langlearn_anki import __version__
from langlearn_anki.ankigen import build_deck, load_media_manifest, result_to_dict

app = typer.Typer(help="langlearn-anki: langlearn-anki CLI")

json_output_enabled = False

_OPT_LANGUAGE = typer.Option(..., help="Target language (e.g. 'de').")
_OPT_DECK = typer.Option(..., help="Deck name.")
_OPT_DATA_DIR = typer.Option(
    ...,
    exists=True,
    file_okay=False,
    dir_okay=True,
    readable=True,
    help="Directory containing cards.json (and media.json if not provided).",
)
_OPT_OUTPUT_PATH = typer.Option(
    None, help="Optional output .apkg path (defaults to data_dir/<deck>.apkg)."
)
_OPT_MEDIA_JSON = typer.Option(
    None, help="Optional media.json path (defaults to data_dir/media.json)."
)


def _emit(payload: Mapping[str, object], text: str) -> None:
    if json_output_enabled:
        typer.echo(json.dumps(payload))
    else:
        typer.echo(text)


@app.callback()
def main(json_output: bool = typer.Option(False, "--json")) -> None:
    "langlearn-anki command group."
    global json_output_enabled
    json_output_enabled = json_output


@app.command()
def version() -> None:
    "Print version."
    _emit({"version": __version__}, __version__)


@app.command()
def doctor() -> None:
    "Check installation health."
    _emit({"status": "ok"}, "ok")


@app.command()
def build(
    language: str = _OPT_LANGUAGE,
    deck: str = _OPT_DECK,
    data_dir: Path = _OPT_DATA_DIR,
    output_path: Path | None = _OPT_OUTPUT_PATH,
    media_json: Path | None = _OPT_MEDIA_JSON,
) -> None:
    "Build an Anki deck from cards.json and provided media assets."
    media = load_media_manifest(media_json, data_dir) if media_json else None
    request = DeckRequest(
        language=language,
        deck=deck,
        data_dir=data_dir,
        media=media,
        output_path=output_path,
    )
    result = build_deck(request)
    _emit(result_to_dict(result), f"deck exported: {result.output_path}")


@app.command()
def install() -> None:
    "Install/configure the tool for the environment."
    payload = {"status": "pending", "message": "install not implemented"}
    _emit(payload, "install not implemented")


@app.command()
def serve() -> None:
    "Start MCP server."
    from langlearn_anki.server import run_server

    run_server()
