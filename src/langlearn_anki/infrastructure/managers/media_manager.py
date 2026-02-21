"""Media file management for deck generation."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import NamedTuple

from langlearn_anki.infrastructure.backends.base import DeckBackend, MediaFile

logger = logging.getLogger(__name__)


class MediaStats(NamedTuple):
    """Media management statistics."""

    files_added: int
    total_size_bytes: int


class MediaManager:
    """Manage media files added to the deck backend."""

    def __init__(self, backend: DeckBackend) -> None:
        self._backend = backend
        self._stats = {
            "files_added": 0,
            "total_size_bytes": 0,
        }

    def add_media_file(self, file_path: str, media_type: str = "") -> MediaFile:
        logger.info(
            "Adding media file: %s (type=%s)",
            file_path,
            media_type,
        )

        if not Path(file_path).exists():
            raise FileNotFoundError(f"Media file does not exist: {file_path}")

        media_file = self._backend.add_media_file(file_path, media_type=media_type)
        self._stats["files_added"] += 1
        try:
            self._stats["total_size_bytes"] += Path(file_path).stat().st_size
        except OSError:
            logger.warning("Could not stat media file: %s", file_path)

        return media_file

    def get_media_stats(self) -> MediaStats:
        return MediaStats(
            files_added=self._stats["files_added"],
            total_size_bytes=self._stats["total_size_bytes"],
        )
