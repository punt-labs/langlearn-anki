from __future__ import annotations

"""Note type mappings for Korean cards.

Uses the legacy record type name ("korean_noun") to align with existing
template and record-processing conventions.
"""

NOTE_TYPE_MAPPINGS: dict[str, str] = {
    "Korean Noun": "korean_noun",
    "Korean Noun with Media": "korean_noun",
}


def get_note_type_mappings() -> dict[str, str]:
    return NOTE_TYPE_MAPPINGS.copy()
