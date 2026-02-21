"""Deck organization utilities."""

from __future__ import annotations

from typing import Any

from langlearn_anki.infrastructure.backends.base import DeckBackend, NoteType


class DeckManager:
    """Manages deck organization and delegates core operations to a backend."""

    def __init__(self, backend: DeckBackend) -> None:
        self._backend = backend
        self._current_subdeck: str | None = None
        self._subdecks: dict[str, str] = {}

    @property
    def backend(self) -> DeckBackend:
        return self._backend

    @property
    def deck_name(self) -> str:
        return self._backend.deck_name

    def set_current_subdeck(self, subdeck_name: str) -> None:
        self._current_subdeck = subdeck_name
        full_deck_name = f"{self._backend.deck_name}::{subdeck_name}"
        self._subdecks[subdeck_name] = full_deck_name
        self._backend.set_current_subdeck(full_deck_name)

    def reset_to_main_deck(self) -> None:
        self._current_subdeck = None
        self._backend.set_current_subdeck(None)

    def get_current_deck_name(self) -> str:
        if self._current_subdeck:
            return self._subdecks[self._current_subdeck]
        return self._backend.deck_name

    def get_subdeck_names(self) -> list[str]:
        return list(self._subdecks.keys())

    def get_full_subdeck_names(self) -> list[str]:
        return list(self._subdecks.values())

    def create_note_type(self, note_type: NoteType) -> str:
        return self._backend.create_note_type(note_type)

    def add_note(
        self,
        note_type_id: str,
        fields: list[str],
        tags: list[str] | None = None,
    ) -> int:
        note_tags = tags or []
        if self._current_subdeck:
            note_tags = [*note_tags, f"subdeck:{self._current_subdeck}"]
        return self._backend.add_note(note_type_id, fields, note_tags)

    def export_deck(self, output_path: str) -> None:
        self._backend.export_deck(output_path)

    def get_stats(self) -> dict[str, Any]:
        stats = self._backend.get_stats()
        stats["subdecks"] = {
            "count": len(self._subdecks),
            "names": self.get_subdeck_names(),
            "full_names": self.get_full_subdeck_names(),
            "current": self._current_subdeck,
        }
        return stats
