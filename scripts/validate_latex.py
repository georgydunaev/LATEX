#!/usr/bin/env python3
"""Validation script for LaTeX macros, styling package, and document examples.

Verifies macro definitions, environment balance, forbidden token invariants,
and compiles document fixtures using pdflatex and bibtex.
"""

import os
import re
import sys
import shutil
import tempfile
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Regex patterns for validation
EMOJI_PATTERN = re.compile(
    r"[\U0001F600-\U0001F64F"  # emoticons
    r"\U0001F300-\U0001F5FF"  # symbols & pictographs
    r"\U0001F680-\U0001F6FF"  # transport & map symbols
    r"\U0001F1E0-\U0001F1FF"  # flags
    r"\U00002702-\U000027B0"
    r"\U000024C2-\U0001F251"
    r"\U0001F900-\U0001F9FF"
    r"\U0001FA70-\U0001FAFF"
    r"]",
    flags=re.UNICODE,
)

FORBIDDEN_ARROWS = ["->", "<-", "=>", "<=", "-->", "<--", "==>", "<=="]


def check_forbidden_tokens(file_path: Path) -> list:
    """Check for emojis or directional arrows in names, titles, or links."""
    errors = []
    text = file_path.read_text(encoding="utf-8", errors="replace")

    # Check emojis
    emoji_matches = EMOJI_PATTERN.findall(text)
    if emoji_matches:
        errors.append(f"{file_path.name}: Contains forbidden emojis: {emoji_matches[:5]}")

    # Check titles/headings/links for directional arrows
    for line_no, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if stripped.startswith(("#", "\\title", "\\section", "\\subsection", "\\caption")):
            for arrow in FORBIDDEN_ARROWS:
                if arrow in stripped:
                    errors.append(f"{file_path.name}:{line_no}: Arrow '{arrow}' in heading/title: {stripped}")

    return errors


def check_balanced_delimiters(file_path: Path) -> list:
    """Check balanced braces and LaTeX environments using stack verification."""
    errors = []
    text = file_path.read_text(encoding="utf-8", errors="replace")

    # Filter out comments
    lines_clean = []
    for line in text.splitlines():
        parts = re.split(r"(?<!\\)%", line, maxsplit=1)
        lines_clean.append(parts[0])
    clean_text = "\n".join(lines_clean)

    # Check balanced curly braces
    open_braces = clean_text.count("{")
    close_braces = clean_text.count("}")
    if open_braces != close_braces:
        errors.append(f"{file_path.name}: Unbalanced curly braces (open={open_braces}, close={close_braces})")

    # Check balanced \\begin and \\end environments using a LIFO stack
    env_tokens = re.findall(r"\\(begin|end)\{([^}]+)\}", clean_text)
    stack = []
    for action, env_name in env_tokens:
        if action == "begin":
            stack.append(env_name)
        elif action == "end":
            if not stack:
                errors.append(f"{file_path.name}: Unexpected \\end{{{env_name}}} with empty stack")
            else:
                top = stack.pop()
                if top != env_name:
                    errors.append(
                        f"{file_path.name}: Mismatched environment: expected \\end{{{top}}}, found \\end{{{env_name}}}"
                    )

    if stack:
        errors.append(f"{file_path.name}: Unclosed environments at EOF: {stack}")

    return errors


def validate_gdmath_package(sty_path: Path) -> list:
    """Validate gdmath.sty package structure and declarations."""
    errors = []
    content = sty_path.read_text(encoding="utf-8")

    if "\\NeedsTeXFormat{LaTeX2e}" not in content:
        errors.append("gdmath.sty: Missing \\NeedsTeXFormat{LaTeX2e}")

    if "\\ProvidesPackage{gdmath}" not in content:
        errors.append("gdmath.sty: Missing \\ProvidesPackage{gdmath}")

    if "\\usepackage{" in content:
        errors.append("gdmath.sty: Uses \\usepackage instead of \\RequirePackage")

    # Check required modular sections
    expected_sections = [
        "Core Package Dependencies",
        "Theorem and Proof Environments",
        "Relational and Definitional Connectives",
        "Mathematical Logic and Proof Theory",
        "Set Theory and Class Theory",
        "Category Theory",
        "Formal Proof Assistants and Type Theory",
        "Semantic Brackets and Delimiters",
    ]
    for section in expected_sections:
        if section not in content:
            errors.append(f"gdmath.sty: Missing modular section '{section}'")

    # Check required core macros
    expected_macros = [
        "\\LRA", "\\defi", "\\eqdef", "\\rsto", "\\propdef",
        "\\Tau", "\\Spec", "\\Const", "\\Var", "\\Func", "\\Pred", "\\Term", "\\Fm",
        "\\Set", "\\Pow", "\\inter", "\\interclass", "\\dom", "\\The", "\\TOrd",
        "\\Ob", "\\Mor", "\\Cat", "\\Hom", "\\Nat", "\\op", "\\id",
        "\\Truej", "\\False", "\\ITerm", "\\allI", "\\exI", "\\exE", "\\judgement",
        "\\llbrack", "\\rrbrack", "\\llbracket", "\\rrbracket", "\\sem", "\\tuple",
    ]
    for macro in expected_macros:
        if macro not in content:
            errors.append(f"gdmath.sty: Expected macro {macro} not found")

    return errors


def test_compile_sample_document(repo_root: Path) -> list:
    """Compile examples/main.tex in a clean temporary directory and verify output."""
    errors = []
    examples_dir = repo_root / "examples"
    main_tex = examples_dir / "main.tex"
    if not main_tex.exists():
        errors.append("examples/main.tex not found")
        return errors

    pdflatex_bin = shutil.which("pdflatex")
    if not pdflatex_bin:
        errors.append("pdflatex binary not found in PATH")
        return errors

    with tempfile.TemporaryDirectory() as temp_dir:
        # Copy examples and gdmath.sty to temp_dir
        dest_examples = Path(temp_dir) / "examples"
        shutil.copytree(examples_dir, dest_examples)
        shutil.copy(repo_root / "gdmath.sty", Path(temp_dir) / "gdmath.sty")

        env = dict(os.environ)
        env["TEXINPUTS"] = f"{temp_dir}:{dest_examples}:"

        # Step 1: First pdflatex pass
        res1 = subprocess.run(
            [pdflatex_bin, "-interaction=nonstopmode", "main.tex"],
            cwd=dest_examples,
            env=env,
            capture_output=True,
            text=True,
        )
        if res1.returncode != 0:
            errors.append(f"First pdflatex pass failed (code {res1.returncode}):\n{res1.stdout[-1000:]}")
            return errors

        # Step 2: bibtex pass
        bibtex_bin = shutil.which("bibtex")
        if bibtex_bin:
            res_bib = subprocess.run(
                [bibtex_bin, "main"],
                cwd=dest_examples,
                env=env,
                capture_output=True,
                text=True,
            )
            if res_bib.returncode != 0:
                errors.append(f"Bibtex pass failed (code {res_bib.returncode}):\n{res_bib.stdout}")

        # Step 3: Second pdflatex pass
        res2 = subprocess.run(
            [pdflatex_bin, "-interaction=nonstopmode", "main.tex"],
            cwd=dest_examples,
            env=env,
            capture_output=True,
            text=True,
        )
        if res2.returncode != 0:
            errors.append(f"Second pdflatex pass failed (code {res2.returncode})")

        # Step 4: Final pdflatex pass
        res3 = subprocess.run(
            [pdflatex_bin, "-interaction=nonstopmode", "main.tex"],
            cwd=dest_examples,
            env=env,
            capture_output=True,
            text=True,
        )
        if res3.returncode != 0:
            errors.append(f"Final pdflatex pass failed (code {res3.returncode})")

        pdf_path = dest_examples / "main.pdf"
        if not pdf_path.exists() or pdf_path.stat().st_size == 0:
            errors.append("main.pdf was not produced or is empty")

    return errors


def main():
    all_errors = []

    # Validate gdmath.sty
    sty_path = REPO_ROOT / "gdmath.sty"
    all_errors.extend(validate_gdmath_package(sty_path))
    all_errors.extend(check_forbidden_tokens(sty_path))
    all_errors.extend(check_balanced_delimiters(sty_path))

    # Validate all .tex files
    tex_files = list(REPO_ROOT.glob("examples/**/*.tex"))
    for tex_file in tex_files:
        all_errors.extend(check_forbidden_tokens(tex_file))
        all_errors.extend(check_balanced_delimiters(tex_file))

    # Validate all markdown docs
    md_files = list(REPO_ROOT.glob("docs/**/*.md")) + list(REPO_ROOT.glob("tickets/**/*.md"))
    for md_file in md_files:
        all_errors.extend(check_forbidden_tokens(md_file))

    # Test compilation
    compile_errors = test_compile_sample_document(REPO_ROOT)
    all_errors.extend(compile_errors)

    if all_errors:
        print("[VALIDATION FAILED]")
        for err in all_errors:
            print(f"  - {err}")
        sys.exit(1)

    print("[VALIDATION PASSED] All macro, syntax, invariant, and compilation checks succeeded.")
    sys.exit(0)


if __name__ == "__main__":
    main()
