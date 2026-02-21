from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast

from langlearn_types import DeckRequest, DeckResult, MediaManifest

from langlearn_anki.infrastructure import (
    AnkiBackend,
    DeckManager,
    MediaManager,
    basic_note_type,
)


@dataclass(frozen=True)
class CardSpec:
    """Single Anki card definition.

    The card references media by ID; media assets must be provided
    via a MediaManifest (no generation happens here).
    """

    front: str
    back: str
    audio_id: str | None = None
    image_id: str | None = None
    tags: tuple[str, ...] = ()


def _resolve_path(base_dir: Path, value: str) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    return base_dir / path


def load_media_manifest(path: Path, base_dir: Path | None = None) -> MediaManifest:
    """Load a media manifest from JSON.

    Expected format:
    {
      "audio": {"id": "relative/or/absolute/path.mp3"},
      "images": {"id": "relative/or/absolute/path.png"}
    }

    Relative paths are resolved against base_dir if provided.
    """
    data_obj = json.loads(path.read_text())
    if not isinstance(data_obj, dict):
        msg = "media.json must be an object"
        raise ValueError(msg)

    data = cast("dict[str, Any]", data_obj)
    audio_raw_obj = data.get("audio", {})
    images_raw_obj = data.get("images", {})
    if not isinstance(audio_raw_obj, dict) or not isinstance(images_raw_obj, dict):
        msg = "media.json must contain 'audio' and 'images' objects"
        raise ValueError(msg)

    audio_raw = cast("dict[str, Any]", audio_raw_obj)
    images_raw = cast("dict[str, Any]", images_raw_obj)

    base = base_dir or path.parent
    audio: dict[str, Path] = {}
    for key, value in audio_raw.items():
        if not isinstance(value, str):
            msg = "media.json audio entries must be string paths"
            raise ValueError(msg)
        audio[key] = _resolve_path(base, value)

    images: dict[str, Path] = {}
    for key, value in images_raw.items():
        if not isinstance(value, str):
            msg = "media.json images entries must be string paths"
            raise ValueError(msg)
        images[key] = _resolve_path(base, value)
    return MediaManifest(audio=audio, images=images, metadata={})


def load_cards(path: Path) -> list[CardSpec]:
    """Load card specs from JSON.

    Expected format:
    [
      {
        "front": "...",
        "back": "...",
        "audio_id": "optional-audio-id",
        "image_id": "optional-image-id",
        "tags": ["optional", "tags"]
      }
    ]
    """
    raw_obj = json.loads(path.read_text())
    if not isinstance(raw_obj, list):
        msg = "cards.json must contain a list of card objects"
        raise ValueError(msg)

    cards: list[CardSpec] = []
    raw_list = cast("list[object]", raw_obj)
    for idx, item in enumerate(raw_list):
        if not isinstance(item, dict):
            msg = f"cards.json entry {idx} must be an object"
            raise ValueError(msg)
        item_dict = cast("dict[str, Any]", item)
        front = item_dict.get("front")
        back = item_dict.get("back")
        if not isinstance(front, str) or not isinstance(back, str):
            msg = f"cards.json entry {idx} must include front/back strings"
            raise ValueError(msg)
        audio_id = item_dict.get("audio_id")
        image_id = item_dict.get("image_id")
        tags_raw = item_dict.get("tags", [])
        if audio_id is not None and not isinstance(audio_id, str):
            msg = f"cards.json entry {idx} audio_id must be a string"
            raise ValueError(msg)
        if image_id is not None and not isinstance(image_id, str):
            msg = f"cards.json entry {idx} image_id must be a string"
            raise ValueError(msg)
        if not isinstance(tags_raw, list):
            msg = f"cards.json entry {idx} tags must be a list of strings"
            raise ValueError(msg)
        tags_list: list[str] = []
        tags_raw_list = cast("list[object]", tags_raw)
        for tag in tags_raw_list:
            if not isinstance(tag, str):
                msg = f"cards.json entry {idx} tags must be a list of strings"
                raise ValueError(msg)
            tags_list.append(tag)
        tags = tuple(tags_list)

        cards.append(
            CardSpec(
                front=front,
                back=back,
                audio_id=audio_id,
                image_id=image_id,
                tags=tags,
            )
        )
    return cards


def _require_media(request: DeckRequest) -> MediaManifest:
    if request.media is not None:
        return request.media

    manifest_path = request.data_dir / "media.json"
    if manifest_path.exists():
        return load_media_manifest(manifest_path, request.data_dir)

    msg = "media manifest is required; langlearn-anki consumes provided media only"
    raise ValueError(msg)


def _validate_media(cards: list[CardSpec], media: MediaManifest) -> None:
    for idx, card in enumerate(cards):
        if card.audio_id and card.audio_id not in media.audio:
            msg = f"cards.json entry {idx} references unknown audio_id"
            raise ValueError(msg)
        if card.image_id and card.image_id not in media.images:
            msg = f"cards.json entry {idx} references unknown image_id"
            raise ValueError(msg)


def build_deck(request: DeckRequest) -> DeckResult:
    """Build an Anki deck from provided card data and media assets.

    This function never generates audio or images. It only consumes
    the media supplied in the DeckRequest or media.json.
    """
    cards_path = request.data_dir / "cards.json"
    if not cards_path.exists():
        msg = "cards.json not found in data_dir"
        raise ValueError(msg)

    cards = load_cards(cards_path)
    media = _require_media(request)
    _validate_media(cards, media)

    output_path = request.output_path or request.data_dir / f"{request.deck}.apkg"

    backend = AnkiBackend(request.deck)
    deck_manager = DeckManager(backend)
    media_manager = MediaManager(backend)

    try:
        note_type_id = deck_manager.create_note_type(basic_note_type())

        audio_files: dict[str, str] = {}
        image_files: dict[str, str] = {}

        for audio_id, path in media.audio.items():
            if not path.exists():
                msg = f"audio file missing: {path}"
                raise ValueError(msg)
            media_file = media_manager.add_media_file(str(path), media_type="audio")
            audio_files[audio_id] = media_file.reference

        for image_id, path in media.images.items():
            if not path.exists():
                msg = f"image file missing: {path}"
                raise ValueError(msg)
            media_file = media_manager.add_media_file(str(path), media_type="image")
            image_files[image_id] = media_file.reference

        used_media: set[str] = set()

        for card in cards:
            front = card.front
            if card.image_id:
                image_reference = image_files[card.image_id]
                front = f'{front}<br><img src="{image_reference}">'
                used_media.add(card.image_id)

            back = card.back
            if card.audio_id:
                audio_reference = audio_files[card.audio_id]
                back = f"{back}<br>{audio_reference}"
                used_media.add(card.audio_id)

            deck_manager.add_note(
                note_type_id, [front, back], list(card.tags) if card.tags else None
            )

        deck_manager.export_deck(str(output_path))
    finally:
        backend.close()

    metadata_obj = getattr(request, "metadata", {})
    metadata = (
        cast("dict[str, str]", metadata_obj) if isinstance(metadata_obj, dict) else {}
    )

    return DeckResult(
        output_path=output_path,
        cards_exported=len(cards),
        media_used=len(used_media),
        metadata=metadata,
    )


def result_to_dict(result: DeckResult) -> dict[str, object]:
    """Serialize DeckResult to a dict suitable for CLI/MCP output."""
    payload: dict[str, object] = {
        "output_path": str(result.output_path),
        "cards_exported": result.cards_exported,
        "media_used": result.media_used,
    }
    if result.metadata:
        payload.update(result.metadata)
    return payload
