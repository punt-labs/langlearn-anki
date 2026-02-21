from __future__ import annotations

from collections.abc import Mapping

from langlearn_anki.languages.german.note_type_mappings import (
    NOTE_TYPE_MAPPINGS as GERMAN_NOTE_TYPE_MAPPINGS,
)
from langlearn_anki.languages.korean.note_type_mappings import (
    NOTE_TYPE_MAPPINGS as KOREAN_NOTE_TYPE_MAPPINGS,
)
from langlearn_anki.languages.russian.note_type_mappings import (
    NOTE_TYPE_MAPPINGS as RUSSIAN_NOTE_TYPE_MAPPINGS,
)

_LANGUAGE_MAPPINGS: dict[str, Mapping[str, str]] = {
    "de": GERMAN_NOTE_TYPE_MAPPINGS,
    "german": GERMAN_NOTE_TYPE_MAPPINGS,
    "ko": KOREAN_NOTE_TYPE_MAPPINGS,
    "korean": KOREAN_NOTE_TYPE_MAPPINGS,
    "ru": RUSSIAN_NOTE_TYPE_MAPPINGS,
    "russian": RUSSIAN_NOTE_TYPE_MAPPINGS,
}


def get_note_type_mappings(language: str) -> dict[str, str]:
    normalized = language.strip().lower()
    return dict(_LANGUAGE_MAPPINGS.get(normalized, {}))
