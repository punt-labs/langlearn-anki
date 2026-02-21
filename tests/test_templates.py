from __future__ import annotations

import pytest

from langlearn_anki.languages import TemplateRepository


def test_template_repository_requires_language() -> None:
    with pytest.raises(ValueError, match="language is required"):
        TemplateRepository("  ")


def test_template_repository_unknown_language() -> None:
    with pytest.raises(ValueError, match="Unsupported language"):
        TemplateRepository("xx")


def test_template_repository_requires_card_type() -> None:
    repo = TemplateRepository("de")
    with pytest.raises(ValueError, match="card_type is required"):
        repo.get_template_files("   ")


def test_template_repository_missing_card_type() -> None:
    repo = TemplateRepository("de")
    with pytest.raises(FileNotFoundError, match="Template file not found"):
        repo.get_template_files("does_not_exist")


def test_template_repository_cache() -> None:
    repo = TemplateRepository("de")
    first = repo.get_template_files("noun")
    second = repo.get_template_files("noun")
    assert first is second


def test_template_repository_language_alias() -> None:
    repo = TemplateRepository("german")
    assert "noun" in repo.list_card_types()


def test_template_repository_get_card_template() -> None:
    repo = TemplateRepository("de")
    card = repo.get_card_template("noun")
    assert card.name == "Card 1"
    assert card.front_html
    assert card.back_html
    assert card.css


def test_template_repository_loads_german_templates() -> None:
    repo = TemplateRepository("de")
    template_files = repo.get_template_files("noun")

    assert template_files.front_html.strip()
    assert template_files.back_html.strip()
    assert template_files.css.strip()

    card_types = repo.list_card_types()
    assert "noun" in card_types
    assert "verb" in card_types


def test_template_repository_loads_korean_templates() -> None:
    repo = TemplateRepository("ko")
    template_files = repo.get_template_files("korean_noun")

    assert template_files.front_html.strip()
    assert template_files.back_html.strip()
    assert template_files.css.strip()
    assert "korean_noun" in repo.list_card_types()


def test_template_repository_loads_russian_templates() -> None:
    repo = TemplateRepository("ru")
    template_files = repo.get_template_files("noun")

    assert template_files.front_html.strip()
    assert template_files.back_html.strip()
    assert template_files.css.strip()
    assert "noun" in repo.list_card_types()
