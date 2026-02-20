# langlearn-anki

Anki deck generation for language learning (media in, decks out).

## Install

```bash
uv tool install punt-langlearn-anki
```

## CLI

```bash
langlearn-anki --help
langlearn-anki --json version
langlearn-anki doctor
langlearn-anki serve
```

## MCP

```bash
langlearn-anki install
langlearn-anki serve
```

## Development

```bash
uv sync --all-extras
uv run ruff check .
uv run ruff format --check .
uv run mypy src/ tests/
uv run pyright src/ tests/
uv run pytest
```
