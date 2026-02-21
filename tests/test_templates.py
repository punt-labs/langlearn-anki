from __future__ import annotations

import pytest

from langlearn_anki.languages import TemplateRepository


def test_template_repository_requires_language() -> None:
    with pytest.raises(ValueError, match="language is required"):
        TemplateRepository("  ")


def test_template_repository_unknown_language() -> None:
    with pytest.raises(ValueError, match="Unsupported language"):
        TemplateRepository("xx")


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
