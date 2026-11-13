#!/usr/bin/env python3
"""Unit tests for LATEX repository, gdmath.sty package, and example fixtures.

Verifies macro definitions, balanced delimiters, package compatibility,
absence of forbidden tokens, and compilation integrity.
"""

import os
import re
import shutil
import tempfile
import unittest
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

EMOJI_PATTERN = re.compile(
    r"[\U0001F600-\U0001F64F"
    r"\U0001F300-\U0001F5FF"
    r"\U0001F680-\U0001F6FF"
    r"\U0001F1E0-\U0001F1FF"
    r"\U00002702-\U000027B0"
    r"\U000024C2-\U0001F251"
    r"\U0001F900-\U0001F9FF"
    r"\U0001FA70-\U0001FAFF"
    r"]",
    flags=re.UNICODE,
)

FORBIDDEN_ARROWS = ["->", "<-", "=>", "<=", "-->", "<--", "==>", "<=="]


class TestMacroDefinitions(unittest.TestCase):
    """Test macro definitions and modular sections in gdmath.sty."""

    @classmethod
    def setUpClass(cls):
        cls.sty_path = REPO_ROOT / "gdmath.sty"
        cls.content = cls.sty_path.read_text(encoding="utf-8")

    def test_package_header(self):
        self.assertIn("\\NeedsTeXFormat{LaTeX2e}", self.content)
        self.assertIn("\\ProvidesPackage{gdmath}", self.content)
        self.assertNotIn("\\usepackage{", self.content, "Package must use \\RequirePackage instead of \\usepackage")

    def test_required_dependencies(self):
        required = ["amsmath", "amsfonts", "amssymb", "amsthm", "mathtools", "float", "hyperref"]
        for pkg in required:
            self.assertIn(f"\\RequirePackage{{{pkg}}}", self.content)

    def test_modular_sections_present(self):
        sections = [
            "Core Package Dependencies",
            "Theorem and Proof Environments",
            "Relational and Definitional Connectives",
            "Mathematical Logic and Proof Theory",
            "Set Theory and Class Theory",
            "Category Theory",
            "Formal Proof Assistants and Type Theory",
            "Semantic Brackets and Delimiters",
        ]
        for sec in sections:
            self.assertIn(sec, self.content)

    def test_logic_macros(self):
        logic_macros = [
            "\\Tau", "\\Spec", "\\Const", "\\Var", "\\Func", "\\Pred",
            "\\Term", "\\Fm", "\\FV", "\\WF", "\\iproof", "\\var",
            "\\term", "\\prop", "\\type", "\\statement",
        ]
        for m in logic_macros:
            self.assertIn(m, self.content)

    def test_set_theory_macros(self):
        set_macros = [
            "\\Set", "\\Pow", "\\inter", "\\interclass", "\\Fun",
            "\\Rel", "\\dom", "\\apo", "\\The", "\\TOrd", "\\Tr", "\\mysucc",
        ]
        for m in set_macros:
            self.assertIn(m, self.content)

    def test_category_theory_macros(self):
        cat_macros = [
            "\\Ob", "\\Mor", "\\Cat", "\\Hom", "\\Nat",
            "\\HomMor", "\\FMor", "\\GMor", "\\op", "\\id", "\\mor",
        ]
        for m in cat_macros:
            self.assertIn(m, self.content)

    def test_proof_assistant_macros(self):
        proof_macros = [
            "\\Truej", "\\ITerm", "\\False", "\\spec",
            "\\allI", "\\exI", "\\exE", "\\judgement", "\\Un", "\\Dd",
        ]
        for m in proof_macros:
            self.assertIn(m, self.content)

    def test_semantic_brackets(self):
        bracket_macros = [
            "\\llbrack", "\\rrbrack", "\\llbracket", "\\rrbracket", "\\sem", "\\tuple",
        ]
        for m in bracket_macros:
            self.assertIn(m, self.content)

    def test_theorem_environments(self):
        envs = ["definition", "lemma", "theorem", "exercise", "corollary", "proposition", "remark", "example"]
        for env in envs:
            self.assertIn(f"{{{env}}}", self.content)


class TestBalancedDelimitersAndSyntax(unittest.TestCase):
    """Test delimiter balance and environment nesting in all TeX files."""

    def test_balanced_curly_braces(self):
        tex_files = [REPO_ROOT / "gdmath.sty"] + list(REPO_ROOT.glob("examples/**/*.tex"))
        for path in tex_files:
            text = path.read_text(encoding="utf-8", errors="replace")
            # Remove comments
            clean_lines = [re.split(r"(?<!\\)%", line, maxsplit=1)[0] for line in text.splitlines()]
            clean_text = "\n".join(clean_lines)
            open_count = clean_text.count("{")
            close_count = clean_text.count("}")
            self.assertEqual(
                open_count, close_count,
                f"File {path.name} has unbalanced curly braces: {open_count} open vs {close_count} close"
            )

    def test_balanced_environments(self):
        tex_files = [REPO_ROOT / "gdmath.sty"] + list(REPO_ROOT.glob("examples/**/*.tex"))
        for path in tex_files:
            text = path.read_text(encoding="utf-8", errors="replace")
            clean_lines = [re.split(r"(?<!\\)%", line, maxsplit=1)[0] for line in text.splitlines()]
            clean_text = "\n".join(clean_lines)
            tokens = re.findall(r"\\(begin|end)\{([^}]+)\}", clean_text)
            stack = []
            for action, env_name in tokens:
                if action == "begin":
                    stack.append(env_name)
                elif action == "end":
                    self.assertTrue(len(stack) > 0, f"Unexpected \\end{{{env_name}}} with empty stack in {path.name}")
                    top = stack.pop()
                    self.assertEqual(
                        top, env_name,
                        f"Mismatched environment in {path.name}: expected \\end{{{top}}}, found \\end{{{env_name}}}"
                    )
            self.assertEqual(len(stack), 0, f"Unclosed environments in {path.name}: {stack}")


class TestInvariantsAndForbiddenTokens(unittest.TestCase):
    """Test adherence to workspace invariants: no emojis, no directional arrows in titles."""

    def test_zero_emojis(self):
        scanned_files = (
            [REPO_ROOT / "gdmath.sty", REPO_ROOT / "Makefile"]
            + list(REPO_ROOT.glob("examples/**/*.tex"))
            + list(REPO_ROOT.glob("docs/**/*.md"))
            + list(REPO_ROOT.glob("tickets/**/*.md"))
            + list(REPO_ROOT.glob("scripts/**/*.py"))
            + list(REPO_ROOT.glob("tests/**/*.py"))
        )
        for path in scanned_files:
            content = path.read_text(encoding="utf-8", errors="replace")
            emojis = EMOJI_PATTERN.findall(content)
            self.assertEqual(emojis, [], f"Forbidden emoji found in {path.name}: {emojis}")

    def test_no_directional_arrows_in_titles(self):
        scanned_files = (
            list(REPO_ROOT.glob("examples/**/*.tex"))
            + list(REPO_ROOT.glob("docs/**/*.md"))
            + list(REPO_ROOT.glob("tickets/**/*.md"))
        )
        for path in scanned_files:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
            for line_no, line in enumerate(lines, start=1):
                stripped = line.strip()
                if stripped.startswith(("#", "\\title", "\\section", "\\subsection", "\\caption")):
                    for arrow in FORBIDDEN_ARROWS:
                        self.assertNotIn(
                            arrow, stripped,
                            f"{path.name}:{line_no} contains directional arrow '{arrow}' in title: {stripped}"
                        )

    def test_no_origin_remote_in_git(self):
        res = subprocess.run(
            ["git", "-C", str(REPO_ROOT), "remote"],
            capture_output=True,
            text=True,
            check=True,
        )
        remotes = res.stdout.splitlines()
        self.assertNotIn("origin", remotes, "Remote 'origin' must never exist; only gitlab and github.")
        self.assertIn("gitlab", remotes, "Remote 'gitlab' must exist.")


class TestPackageCompatibilityAndCompilation(unittest.TestCase):
    """Test LaTeX compilation and package collision resistance."""

    def test_idempotent_package_loading(self):
        """Loading gdmath.sty twice must not trigger duplicate command errors."""
        pdflatex_bin = shutil.which("pdflatex")
        if not pdflatex_bin:
            self.skipTest("pdflatex not installed")

        fixture = r"""\documentclass{article}
\usepackage{gdmath}
\usepackage{gdmath}
\begin{document}
\[ \sem{\Tau} \eqdef \tuple{\Ob(\Cat), \dom(f)} \]
\end{document}
"""
        with tempfile.TemporaryDirectory() as td:
            tex_file = Path(td) / "idempotent.tex"
            tex_file.write_text(fixture, encoding="utf-8")
            shutil.copy(REPO_ROOT / "gdmath.sty", Path(td) / "gdmath.sty")

            res = subprocess.run(
                [pdflatex_bin, "-interaction=nonstopmode", "idempotent.tex"],
                cwd=td,
                capture_output=True,
                text=True,
            )
            self.assertEqual(
                res.returncode, 0,
                f"Idempotent package loading failed with code {res.returncode}:\n{res.stdout[-800:]}"
            )

    def test_validation_script_passes(self):
        """Run validation script and ensure exit code 0."""
        script_path = REPO_ROOT / "scripts" / "validate_latex.py"
        res = subprocess.run(
            ["python3", str(script_path)],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
        )
        self.assertEqual(
            res.returncode, 0,
            f"Validation script failed:\n{res.stdout}\n{res.stderr}"
        )


if __name__ == "__main__":
    unittest.main()
