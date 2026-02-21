from __future__ import annotations

from dataclasses import dataclass
from importlib import resources
from importlib.resources.abc import Traversable

from langlearn_anki.infrastructure.backends import CardTemplate

_LANGUAGE_PACKAGES: dict[str, str] = {
    "de": "langlearn_anki.languages.german",
    "german": "langlearn_anki.languages.german",
    "ko": "langlearn_anki.languages.korean",
    "korean": "langlearn_anki.languages.korean",
    "ru": "langlearn_anki.languages.russian",
    "russian": "langlearn_anki.languages.russian",
}

_LANGUAGE_LOCALES: dict[str, str] = {
    "de": "DE_de",
    "german": "DE_de",
    "ko": "KO_ko",
    "korean": "KO_ko",
    "ru": "RU_ru",
    "russian": "RU_ru",
}


@dataclass(frozen=True)
class TemplateFiles:
    front_html: str
    back_html: str
    css: str


class TemplateRepository:
    """Load HTML/CSS templates for language-specific card types."""

    def __init__(self, language: str) -> None:
        normalized = language.strip().lower()
        if not normalized:
            msg = "language is required"
            raise ValueError(msg)
        if normalized not in _LANGUAGE_PACKAGES:
            msg = f"Unsupported language: {language}"
            raise ValueError(msg)

        self._language = normalized
        self._locale = _LANGUAGE_LOCALES[normalized]
        package = _LANGUAGE_PACKAGES[normalized]
        self._templates_dir = resources.files(package) / "templates"
        if not self._templates_dir.is_dir():
            msg = f"Template directory missing for language: {language}"
            raise FileNotFoundError(msg)
        self._cache: dict[str, TemplateFiles] = {}

    def get_template_files(self, card_type: str) -> TemplateFiles:
        card_key = card_type.strip()
        if not card_key:
            msg = "card_type is required"
            raise ValueError(msg)
        cached = self._cache.get(card_key)
        if cached is not None:
            return cached

        template_files = self._load_template_files(card_key)
        self._cache[card_key] = template_files
        return template_files

    def get_card_template(
        self, card_type: str, name: str | None = None
    ) -> CardTemplate:
        template_files = self.get_template_files(card_type)
        return CardTemplate(
            name=name or "Card 1",
            front_html=template_files.front_html,
            back_html=template_files.back_html,
            css=template_files.css,
        )

    def list_card_types(self) -> list[str]:
        card_types: set[str] = set()
        locale_suffix = f"_{self._locale}"
        for entry in self._templates_dir.iterdir():
            if not entry.is_file():
                continue
            name = entry.name
            if not name.endswith(".html"):
                continue
            stem = name[: -len(".html")]
            if not stem.endswith("_front"):
                continue
            base = stem[: -len("_front")]
            if base.endswith(locale_suffix):
                base = base[: -len(locale_suffix)]
            if base:
                card_types.add(base)
        return sorted(card_types)

    def _load_template_files(self, card_type: str) -> TemplateFiles:
        front_file = self._resolve_template_file(card_type, "front", ".html")
        back_file = self._resolve_template_file(card_type, "back", ".html")
        css_file = self._resolve_template_file(card_type, "", ".css")

        return TemplateFiles(
            front_html=self._read_text(front_file),
            back_html=self._read_text(back_file),
            css=self._read_text(css_file),
        )

    def _resolve_template_file(
        self, card_type: str, side: str, suffix: str
    ) -> Traversable:
        side_suffix = f"_{side}" if side else ""
        candidates = [
            f"{card_type}_{self._locale}{side_suffix}{suffix}",
            f"{card_type}{side_suffix}{suffix}",
        ]
        for filename in candidates:
            candidate = self._templates_dir / filename
            if candidate.is_file():
                return candidate
        msg = (
            f"Template file not found for card_type={card_type} "
            f"side={side} candidates={candidates}"
        )
        raise FileNotFoundError(msg)

    @staticmethod
    def _read_text(path: Traversable) -> str:
        return path.read_text(encoding="utf-8")
