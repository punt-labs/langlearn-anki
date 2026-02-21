from __future__ import annotations

from langlearn_anki.languages import get_note_type_mappings


def test_get_note_type_mappings() -> None:
    german = get_note_type_mappings("de")
    assert german["German Noun"] == "noun"
    assert get_note_type_mappings("unknown") == {}
