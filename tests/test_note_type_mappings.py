from __future__ import annotations

from langlearn_anki.languages import get_note_type_mappings
from langlearn_anki.languages.german.note_type_mappings import (
    NOTE_TYPE_MAPPINGS as GERMAN_NOTE_TYPE_MAPPINGS,
)
from langlearn_anki.languages.korean.note_type_mappings import (
    NOTE_TYPE_MAPPINGS as KOREAN_NOTE_TYPE_MAPPINGS,
)
from langlearn_anki.languages.russian.note_type_mappings import (
    NOTE_TYPE_MAPPINGS as RUSSIAN_NOTE_TYPE_MAPPINGS,
)


def test_get_note_type_mappings_german() -> None:
    german = get_note_type_mappings("de")
    assert german == GERMAN_NOTE_TYPE_MAPPINGS
    assert german["German Noun"] == "noun"


def test_get_note_type_mappings_korean() -> None:
    korean = get_note_type_mappings("ko")
    assert korean == KOREAN_NOTE_TYPE_MAPPINGS
    assert korean["Korean Noun"] == "korean_noun"


def test_get_note_type_mappings_russian() -> None:
    russian = get_note_type_mappings("ru")
    assert russian == RUSSIAN_NOTE_TYPE_MAPPINGS
    assert russian["Russian Noun"] == "noun"


def test_get_note_type_mappings_aliases() -> None:
    assert get_note_type_mappings("de") == get_note_type_mappings("german")
    assert get_note_type_mappings("ko") == get_note_type_mappings("korean")
    assert get_note_type_mappings("ru") == get_note_type_mappings("russian")


def test_get_note_type_mappings_unknown_language() -> None:
    assert get_note_type_mappings("unknown") == {}
