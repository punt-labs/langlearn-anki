# langlearn-anki

Anki deck generation for language learning (media in, decks out).

## Status (2026-02-21)
- `build` consumes `cards.json` and `media.json` and exports a basic Front/Back deck.
- Media is required and never generated inside this package.
- Template library exists (German, Korean, Russian) but is not wired into deck generation yet.

## Roadmap
See ROADMAP.md.

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

Example:

```bash
langlearn-anki build --language de --deck "Demo" --data-dir ./data
```

## Data format

`cards.json` example:

```json
[
  {"front": "Hallo", "back": "Hello", "audio_id": "a1", "image_id": "i1", "tags": ["demo"]}
]
```

`media.json` example:

```json
{
  "audio": {"a1": "audio/hallo.mp3"},
  "images": {"i1": "images/hallo.png"}
}
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
