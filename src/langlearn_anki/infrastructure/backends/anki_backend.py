"""Official Anki backend implementation for deck generation."""

from __future__ import annotations

import os
import shutil
import tempfile
import unicodedata
from pathlib import Path
from typing import Any, cast

from anki.collection import Collection
from anki.decks import DeckId
from anki.exporting import AnkiPackageExporter
from anki.models import NotetypeId

from .base import CardTemplate, DeckBackend, MediaFile, NoteType


class AnkiBackend(DeckBackend):
    """Deck backend using the official Anki library."""

    def __init__(self, deck_name: str, description: str = "") -> None:
        super().__init__(deck_name, description)
        self._temp_dir = tempfile.mkdtemp()
        self._collection_path = os.path.join(self._temp_dir, "collection.anki2")
        self._collection = Collection(self._collection_path)

        main_deck_id = self._collection.decks.add_normal_deck_with_name(deck_name).id
        self._main_deck_id: DeckId = DeckId(main_deck_id)
        self._deck_id: DeckId = self._main_deck_id
        self._subdeck_map: dict[str, DeckId] = {}

        self._note_type_map: dict[str, NotetypeId] = {}
        self._next_note_type_id = 1

    def close(self) -> None:
        """Close the Anki collection and clean up temp files."""
        if hasattr(self, "_collection"):
            self._collection.close()
        if hasattr(self, "_temp_dir") and os.path.exists(self._temp_dir):
            shutil.rmtree(self._temp_dir, ignore_errors=True)

    def __del__(self) -> None:
        self.close()

    def create_note_type(self, note_type: NoteType) -> str:
        existing = self._collection.models.by_name(note_type.name)
        if existing is not None:
            existing_id = existing.get("id")
            if isinstance(existing_id, int):
                note_type_id = str(self._next_note_type_id)
                self._note_type_map[note_type_id] = NotetypeId(existing_id)
                self._next_note_type_id += 1
                return note_type_id

        notetype = self._collection.models.new(note_type.name)
        for field_name in note_type.fields:
            field = self._collection.models.new_field(field_name)
            self._collection.models.add_field(notetype, field)

        for template in note_type.templates:
            card_template = self._collection.models.new_template(template.name)
            card_template["qfmt"] = template.front_html
            card_template["afmt"] = template.back_html
            self._collection.models.add_template(notetype, card_template)

        if note_type.templates:
            notetype["css"] = note_type.templates[0].css

        changes_with_id = self._collection.models.add(notetype)
        actual_notetype_id = changes_with_id.id

        note_type_id = str(self._next_note_type_id)
        self._note_type_map[note_type_id] = NotetypeId(actual_notetype_id)
        self._next_note_type_id += 1
        return note_type_id

    def set_current_subdeck(self, full_deck_name: str | None) -> None:
        if full_deck_name is None:
            self._deck_id = self._main_deck_id
            return

        if full_deck_name not in self._subdeck_map:
            subdeck_id = self._collection.decks.add_normal_deck_with_name(
                full_deck_name
            ).id
            self._subdeck_map[full_deck_name] = DeckId(subdeck_id)

        self._deck_id = self._subdeck_map[full_deck_name]

    def add_note(
        self,
        note_type_id: str,
        fields: list[str],
        tags: list[str] | None = None,
    ) -> int:
        if note_type_id not in self._note_type_map:
            raise ValueError(f"Note type ID not found: {note_type_id}")

        anki_notetype_id = self._note_type_map[note_type_id]
        notetype = self._collection.models.get(anki_notetype_id)
        if notetype is None:
            raise ValueError(f"Note type not found: {anki_notetype_id}")

        note = self._collection.new_note(notetype)
        for i, value in enumerate(fields):
            if i < len(note.fields):
                note.fields[i] = value

        if tags:
            note.tags = tags

        self._collection.add_note(note, self._deck_id)
        return int(note.id)

    def add_media_file(self, file_path: str, media_type: str = "") -> MediaFile:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Media file not found: {file_path}")

        filename = self._collection.media.add_file(file_path)
        normalized_filename = unicodedata.normalize("NFC", filename)

        if media_type == "audio":
            reference = f"[sound:{normalized_filename}]"
        elif media_type == "image":
            reference = normalized_filename
        elif media_type == "":
            extension = Path(filename).suffix.lower()
            if extension == ".mp3":
                reference = f"[sound:{normalized_filename}]"
            elif extension in {".jpg", ".jpeg", ".png"}:
                reference = normalized_filename
            else:
                raise ValueError(f"Cannot infer media type from extension: {extension}")
        else:
            raise ValueError(f"Unknown media type: {media_type}")

        media_file = MediaFile(
            path=file_path, reference=reference, media_type=media_type
        )
        self._media_files.append(media_file)
        return media_file

    def export_deck(self, output_path: str) -> None:
        exporter = AnkiPackageExporter(self._collection)
        exporter.did = self._deck_id
        exporter_any = cast("Any", exporter)
        if hasattr(exporter_any, "include_media"):
            exporter_any.include_media = True

        export_to_file = getattr(exporter_any, "export_to_file", None)
        if callable(export_to_file):
            export_to_file(output_path)
            return

        export_into = getattr(exporter_any, "exportInto", None)
        if callable(export_into):
            export_into(output_path)
            return

        raise RuntimeError("No supported export method found")

    def get_stats(self) -> dict[str, Any]:
        stats: dict[str, Any] = {
            "deck_name": self.deck_name,
            "note_types_count": len(self._note_type_map),
            "notes_count": 0,
            "media_files_count": len(self._media_files),
        }

        try:
            if self._collection.db is not None:
                stats["notes_count"] = self._collection.db.scalar(
                    "SELECT count() FROM notes"
                )
        except Exception:
            stats["notes_count"] = 0

        return stats


def basic_note_type() -> NoteType:
    """Return a simple default note type definition."""
    return NoteType(
        name="Langlearn Basic",
        fields=["Front", "Back"],
        templates=[
            CardTemplate(
                name="Card 1",
                front_html="{{Front}}",
                back_html='{{FrontSide}}<hr id="answer">{{Back}}',
                css="",
            )
        ],
    )
