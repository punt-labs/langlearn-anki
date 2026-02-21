from __future__ import annotations

NOTE_TYPE_MAPPINGS: dict[str, str] = {
    "Russian Noun": "noun",
    "Russian Noun with Media": "noun",
}


def get_note_type_mappings() -> dict[str, str]:
    return NOTE_TYPE_MAPPINGS.copy()
