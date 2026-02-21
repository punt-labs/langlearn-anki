from __future__ import annotations

NOTE_TYPE_MAPPINGS: dict[str, str] = {
    "Korean Noun": "korean_noun",
    "Korean Noun with Media": "korean_noun",
}


def get_note_type_mappings() -> dict[str, str]:
    return NOTE_TYPE_MAPPINGS.copy()
