from __future__ import annotations

from pathlib import Path
from typing import Any, cast

import pytest

from langlearn_anki.infrastructure import AnkiBackend, DeckManager, MediaManager
from langlearn_anki.infrastructure.backends import basic_note_type


def test_anki_backend_add_note_rejects_extra_fields(tmp_path: Path) -> None:
    backend = AnkiBackend("Demo")
    try:
        note_type_id = backend.create_note_type(basic_note_type())
        with pytest.raises(ValueError, match="Too many fields"):
            backend.add_note(note_type_id, ["one", "two", "three"])
    finally:
        backend.close()


def test_anki_backend_export_uses_main_deck(tmp_path: Path) -> None:
    backend = AnkiBackend("Demo")
    try:
        note_type_id = backend.create_note_type(basic_note_type())
        backend.set_current_subdeck("Subdeck")
        backend.add_note(note_type_id, ["front", "back"])

        output_path = tmp_path / "demo.apkg"
        backend.export_deck(str(output_path))
        assert output_path.exists()
    finally:
        backend.close()


def test_anki_backend_close_cleans_temp_dir(tmp_path: Path) -> None:
    backend = AnkiBackend("Demo")
    temp_dir = Path(cast("Any", backend)._temp_dir)
    backend.close()
    assert not temp_dir.exists()


def test_deck_manager_tracks_subdeck() -> None:
    backend = AnkiBackend("Demo")
    try:
        manager = DeckManager(backend)
        manager.set_current_subdeck("Verbs")
        assert "::" in manager.get_current_deck_name()
    finally:
        backend.close()


def test_media_manager_adds_audio_file(tmp_path: Path) -> None:
    backend = AnkiBackend("Demo")
    try:
        manager = MediaManager(backend)
        audio_path = tmp_path / "hello.mp3"
        audio_path.write_text("audio")
        media = manager.add_media_file(str(audio_path), media_type="audio")
        assert media.reference.startswith("[sound:")
    finally:
        backend.close()
