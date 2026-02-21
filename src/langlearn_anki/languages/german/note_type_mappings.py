from __future__ import annotations

NOTE_TYPE_MAPPINGS: dict[str, str] = {
    "German Noun": "noun",
    "German Noun with Media": "noun",
    "German Adjective": "adjective",
    "German Adjective with Media": "adjective",
    "German Adverb": "adverb",
    "German Adverb with Media": "adverb",
    "German Negation": "negation",
    "German Negation with Media": "negation",
    "German Verb": "verb",
    "German Verb with Media": "verb",
    "German Phrase": "phrase",
    "German Phrase with Media": "phrase",
    "German Preposition": "preposition",
    "German Preposition with Media": "preposition",
    "German Artikel Gender with Media": "artikel_gender",
    "German Artikel Context with Media": "artikel_context",
    "German Noun_Case_Context with Media": "noun_case_context",
    "German Noun_Article_Recognition with Media": "noun_article_recognition",
}


def get_note_type_mappings() -> dict[str, str]:
    return NOTE_TYPE_MAPPINGS.copy()
