from __future__ import annotations

import json
from pathlib import Path

import pytest
from langlearn_types import DeckRequest

from langlearn_anki.ankigen import build_deck


def _write_text(path: Path, text: str = "x") -> None:
    path.write_text(text)


def test_build_deck_requires_media_manifest(tmp_path: Path) -> None:
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    (data_dir / "cards.json").write_text("[]")

    request = DeckRequest(
        language="de",
        deck="Demo",
        data_dir=data_dir,
        media=None,
        output_path=tmp_path / "demo.apkg",
    )

    with pytest.raises(ValueError, match="media manifest is required"):
        build_deck(request)


def test_build_deck_with_media_json(tmp_path: Path) -> None:
    data_dir = tmp_path / "data"
    data_dir.mkdir()

    audio_path = data_dir / "audio.mp3"
    image_path = data_dir / "image.png"
    _write_text(audio_path, "audio")
    _write_text(image_path, "image")

    media = {
        "audio": {"a1": "audio.mp3"},
        "images": {"i1": "image.png"},
    }
    (data_dir / "media.json").write_text(json.dumps(media))

    cards = [
        {
            "front": "Hallo",
            "back": "Hello",
            "audio_id": "a1",
            "image_id": "i1",
            "tags": ["basic"],
        }
    ]
    (data_dir / "cards.json").write_text(json.dumps(cards))

    output_path = tmp_path / "demo.apkg"
    request = DeckRequest(
        language="de",
        deck="Demo",
        data_dir=data_dir,
        media=None,
        output_path=output_path,
    )

    result = build_deck(request)

    assert result.cards_exported == 1
    assert result.media_used == 2
    assert result.output_path == output_path
    assert output_path.exists()
