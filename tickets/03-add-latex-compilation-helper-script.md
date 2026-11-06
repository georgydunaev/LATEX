# Ticket 03: Add safe non-interactive pdflatex compilation bash script

**Project:** LATEX
**Importance:** 3/10
**State:** opened
**Target Model Tier:** Tier 2 / Tier 3 (Free Cloud / Small LLMs)
**Labels:** user, simple-task, tier2-model, tier3-model, LATEX

## Description
Create `compile_tex.sh` in `LATEX/` that runs `pdflatex -interaction=nonstopmode -halt-on-error "$1"`, cleans up temporary `.aux`, `.log`, `.out` files on success, and prints clean exit code.

## Acceptance Criteria
1. Implementation is clean, tested, and self-contained within `LATEX/`.
2. Do not modify files outside `LATEX/`.
3. Verify syntax and tests pass without errors.
