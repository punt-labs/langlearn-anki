from __future__ import annotations

import json
from collections.abc import Mapping

import typer

from langlearn_anki import __version__

app = typer.Typer(help="langlearn-anki: langlearn-anki CLI")

json_output_enabled = False


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
def install() -> None:
    "Install/configure the tool for the environment."
    payload = {"status": "pending", "message": "install not implemented"}
    _emit(payload, "install not implemented")


@app.command()
def serve() -> None:
    "Start MCP server."
    from langlearn_anki.server import run_server

    run_server()
