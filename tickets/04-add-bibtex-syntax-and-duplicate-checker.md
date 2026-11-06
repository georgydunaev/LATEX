# Ticket 04: Add BibTeX entry syntax and duplicate key validator script

**Project:** LATEX
**Importance:** 3/10
**State:** opened
**Target Model Tier:** Tier 2 / Tier 3 (Free Cloud / Small LLMs)
**Labels:** user, simple-task, tier2-model, tier3-model, LATEX

## Description
Create `check_bibtex.py` in `LATEX/` that parses `.bib` files, checks for duplicate citation keys, verifies balanced braces, and warns if required fields (`author`, `title`, `year`) are missing.

## Acceptance Criteria
1. Implementation is clean, tested, and self-contained within `LATEX/`.
2. Do not modify files outside `LATEX/`.
3. Verify syntax and tests pass without errors.
