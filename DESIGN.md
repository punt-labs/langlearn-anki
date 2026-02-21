# Design Decision Log

## 0001 — Initial split into tri-modal packages (SETTLED)
- Deck builder consumes pre-generated media assets only.
- No audio or image generation logic in this package.

## 0002 — Templates live with the Anki backend (SETTLED)
- HTML/CSS templates are owned and shipped by langlearn-anki.
- Orchestrator supplies fields and media references; template rendering happens here.
