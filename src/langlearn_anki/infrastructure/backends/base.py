"""Core interfaces for Anki deck backends."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class MediaFile:
    """Represents a media file added to an Anki collection."""

    path: str
    reference: str
    media_type: str = ""


@dataclass(frozen=True)
class CardTemplate:
    """Represents a card template with front/back HTML and CSS."""

    name: str
    front_html: str
    back_html: str
    css: str = ""


@dataclass(frozen=True)
class NoteType:
    """Represents a note type (model) with fields and templates."""

    name: str
    fields: list[str]
    templates: list[CardTemplate]


class DeckBackend(ABC):
    """Abstract base class for deck generation backends."""

    def __init__(self, deck_name: str, description: str = "") -> None:
        self.deck_name = deck_name
        self.description = description
        self._media_files: list[MediaFile] = []

    @abstractmethod
    def create_note_type(self, note_type: NoteType) -> str:
        """Create a note type and return its identifier."""

    @abstractmethod
    def add_note(
        self,
        note_type_id: str,
        fields: list[str],
        tags: list[str] | None = None,
    ) -> int:
        """Add a note to the deck and return its ID."""

    @abstractmethod
    def add_media_file(self, file_path: str, media_type: str = "") -> MediaFile:
        """Add a media file to the deck and return its reference."""

    @abstractmethod
    def export_deck(self, output_path: str) -> None:
        """Export the deck to a file."""

    @abstractmethod
    def get_stats(self) -> dict[str, Any]:
        """Return statistics about the deck."""

    def get_media_files(self) -> list[MediaFile]:
        """Return the media files added to this backend."""
        return self._media_files.copy()

    def set_current_subdeck(self, full_deck_name: str | None) -> None:
        """Set the current subdeck (default: no-op)."""
        _ = full_deck_name
