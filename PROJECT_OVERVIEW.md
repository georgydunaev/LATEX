# Project Overview: Canonical Mathematical LaTeX Style and Validation Suite (`LATEX`)

## 1. Purpose and Scope
`LATEX` (`/botworkspace/LATEX`) houses the canonical LaTeX style package (`gdmath.sty`) used across `/botworkspace` for mathematical logic, Zermelo-Fraenkel (`ZFC`), Von Neumann-Bernays-Goedel (`NBG`), and Morse-Kelley (`MK`) class theories, category theory, and semantic brackets, along with multi-chapter example documents and an automated LaTeX macro/AST validator. All stored `.pdf` files are strictly immutable per Fact 11.

## 2. Architecture and Key Files
- [gdmath.sty](file:///botworkspace/LATEX/gdmath.sty) — Canonical LaTeX macro package defining theorem environments (`thm`, `lem`, `prop`, `cor`, `defn`, `rem`, `exm`), proof markers (`\myprf`, `\myqed`), definitional equality macros (`\eqdef`, `\propdef`), set/class builders, and semantic brackets.
- [REPOSITORY_CATALOG_AND_NOTES.md](file:///botworkspace/LATEX/REPOSITORY_CATALOG_AND_NOTES.md) — Line-by-line catalog of macros and environments in `gdmath.sty`.
- `docs/` — Macro reference documentation (`docs/MACRO_REFERENCE.md`).
- `chapters/` and `examples/` — Modular LaTeX chapters and sample documents demonstrating `gdmath.sty` usage.
- `scripts/` — Automated LaTeX syntax, brace-balance, and macro validator (`scripts/validate_latex.py`).
- `tests/` — Automated Python unit test suite verifying `gdmath.sty` macro definitions and validation rules.

## 3. Verification
```bash
python3 -m unittest discover -s /botworkspace/LATEX/tests -p "test_*.py"
```
