# LaTeX Mathematical Styling Package Reference (gdmath.sty)

## Overview

The `gdmath.sty` package provides standardized mathematical logic, set theory, category theory, proof assistant notation, theorem environments, and semantic delimiters for mathematical documents and formal proof literature.

## Module Index

1. Core Package Dependencies
2. Theorem and Proof Environments
3. Relational and Definitional Connectives
4. Mathematical Logic and Proof Theory
5. Set Theory and Class Theory
6. Category Theory
7. Formal Proof Assistants and Type Theory
8. Semantic Brackets and Delimiters
9. MKTD1 / MKTD2 Frameworks, Dunaev Tagged Pairs, and Variable-Binding Operators

---

## 1. Core Package Dependencies

The package automatically requires standard mathematical and formatting packages without duplicate inclusion:
- `amsmath`
- `amsfonts`
- `amssymb`
- `amsthm`
- `mathtools`
- `float`
- `hyperref`

It defines `\DeclareMathOperatorSafe` to prevent collisions when re-importing or combining packages.

---

## 2. Theorem and Proof Environments

The following theorem environments are declared under `\theoremstyle{definition}` with section-scoped numbering:
- `definition`
- `lemma`
- `theorem`
- `exercise`
- `corollary`
- `proposition`
- `remark`
- `example`

Proof shorthands:
- `\myprf`: Produces bold prefix `Proof.` without indentation.
- `\myqed`: Flushes bold `Q.E.D.` to the right margin.

---

## 3. Relational and Definitional Connectives

| Macro | Rendered Expansion | Meaning |
|---|---|---|
| `\LRA` | `\Longleftrightarrow` | Logical equivalence (if and only if) |
| `\defi` | `\mathrm{def}` | Definition tag |
| `\eqdef` | `\stackrel{\defi}{=}` | Equality by definition |
| `\rsto` | `\stackrel{\mathrm{RS}}{\to}` | Reduction step relation |
| `\propdef` | `\stackrel{\defi}{\ \Longleftrightarrow\ }` | Propositional equivalence by definition |

---

## 4. Mathematical Logic and Proof Theory

| Macro | Type | Description |
|---|---|---|
| `\Tau` | Symbol | Formal theory or signature Tau |
| `\Spec` | Operator | Specification function |
| `\Const` | Operator | Constant symbols |
| `\Var` | Operator | Variable symbols |
| `\Func` | Operator | Function symbols |
| `\Pred` | Operator | Predicate symbols |
| `\Term` | Operator | Set of terms |
| `\Fm` | Operator | Set of formulas |
| `\FV` | Operator | Free variables |
| `\WF` | Operator | Well-formed formulas or terms |
| `\iproof` | Operator | Inductive proof constructor |
| `\var` | Operator | Variable judgment |
| `\term` | Operator | Term judgment |
| `\prop` | Operator | Proposition judgment |
| `\type` | Operator | Type judgment |
| `\statement` | Operator | Statement judgment |

---

## 5. Set Theory and Class Theory

| Macro | Type | Description |
|---|---|---|
| `\Set` | Operator | Set predicate or universe |
| `\Pow` | Symbol | Power set operator |
| `\inter` | Big Operator | Big intersection operator |
| `\interclass` | Big Operator | Class-indexed intersection operator |
| `\Fun` | Operator | Function space predicate |
| `\Rel` | Operator | Binary relation predicate |
| `\dom` | Operator | Domain of a relation or function |
| `\apo` | Symbol | Apostrophe prime mark |
| `\The` | Operator | Definite description operator |
| `\TOrd` | Operator | Transitive ordinal predicate |
| `\Tr` | Operator | Transitive set predicate |
| `\mysucc` | Operator | Successor ordinal constructor |

---

## 6. Category Theory

| Macro | Type | Description |
|---|---|---|
| `\Ob` | Operator | Objects of a category |
| `\Mor` | Operator | Morphisms of a category |
| `\Cat` | Operator | Category universe or collection |
| `\Hom` | Operator | Hom-set constructor |
| `\Nat` | Operator | Natural transformations |
| `\HomMor` | Symbol | Lifted hom-morphism functor |
| `\FMor` | Symbol | Lifted functor action on morphisms |
| `\GMor` | Symbol | Secondary lifted functor action |
| `\op` | Operator | Opposite category superscript |
| `\id` | Operator | Identity morphism |
| `\mor` | Operator | Morphism judgment |

---

## 7. Formal Proof Assistants and Type Theory

| Macro | Type | Description |
|---|---|---|
| `\Truej` | Operator | Truth judgment |
| `\False` | Operator | Falsehood judgment |
| `\ITerm` | Operator | Isabelle / Obelisk term constructor |
| `\spec` | Operator | Specialization inference rule |
| `\allI` | Operator | Universal quantifier introduction rule |
| `\exI` | Operator | Existential quantifier introduction rule |
| `\exE` | Operator | Existential quantifier elimination rule |
| `\judgement` | Operator | Generic judgment constructor |
| `\Un` | Symbol | Universal class or universe |
| `\Dd` | Symbol | Domain or derivation class |

---

## 8. Semantic Brackets and Delimiters

| Macro | Expansion | Description |
|---|---|---|
| `\llbrack` / `\rrbrack` | `[\![` / `]\!]` | Semantic evaluation brackets |
| `\llbracket` / `\rrbracket` | `[\![` / `]\!]` | Semantic denotation brackets |
| `\sem{x}` | `\llbracket x \rrbracket` | Full semantic bracket wrapper |
| `\tuple{x}` | `\langle x \rangle` | Ordered tuple enclosure |
| `\cornerquote{x}` | `\ulcorner x \urcorner` | Gödel / corner quote enclosure |

---

## 9. MKTD1 / MKTD2 Frameworks, Dunaev Tagged Pairs, and Variable-Binding Operators

Demonstrated in `chapters/05_mktd1_mktd2_binders.tex` (and `examples/chapters/05_mktd1_mktd2_binders.tex`):

| Macro | Expansion | Description |
|---|---|---|
| `\mktdseq{G}{p}` | `G \vdash_{\mathrm{MKTD1}} p` | MKTD1-theory sequent derivability judgment |
| `\mktdthseq{W}{G}{p}` | `W ; G \vdash_{\mathrm{MKTD1}} p` | Theory-scoped MKTD1-theory sequent judgment |
| `\ClassExpre` / `\FmExpre` / `\TheoryExpre` | Operator | Typed SML AST expression sorts in MKTD1-system |
| `\CtxExpre` / `\StmtExpre` / `\PrfExpre` | Operator | Context, statement, and proof expression sorts in MKTD1-system |
| `\isSet` | Operator | Set-hood predicate in NBG / MK class theory |
| `\mktdty{G}{t}{T}` | `G \vdash_{\mathrm{MKTD2}} t : T` | MKTD2-theory constructive typing judgment |
| `\DepProd{x}{A}{B}` | `\prod_{x : A} B` | Dependent product type in MKTD2-framework |
| `\DepSum{x}{A}{B}` | `\sum_{x : A} B` | Dependent sum type in MKTD2-framework |
| `\LamTerm{x}{A}{t}` | `\lambda (x : A).\, t` | Typed lambda proof term in MKTD2-framework |
| `\DepPair{a}{b}` | `\langle a , b \rangle_{\Sigma}` | Dependent pair constructor in MKTD2-framework |
| `\dtagL{X}` / `\dtagR{Y}` | `\{X, \varnothing\}` / `\{\{Y\}, \{\varnothing\}\}` | Left and right Dunaev class element tags |
| `\dpair{X}{Y}` | `\langle X , Y \rangle_{\mathrm{D}}` | Dunaev tagged ordered pair for arbitrary classes |
| `\dpairdef{X}{Y}` | `\dtagL{X} \cup \dtagR{Y}` | Definitional expansion of Dunaev tagged ordered pair |
| `\bforall{x}{p}` / `\bexists{x}{p}` | `\forall x.\, p` / `\exists x.\, p` | Universal and existential quantifier binders |
| `\bexistsuniq{x}{p}` / `\buniq{x}{p}` | `\exists! x.\, p` / `! x.\, p` | Unique existence and uniqueness quantifier binders |
| `\bkappa{x}{p}` / `\bclasscomp{x}{p}` | `\kappa x.\, p` / `\{x \mid p\}` | Class comprehension binder (over `Class` variables) |
| `\biota{x}{p}` | `\iota x.\, p` | Definite description binder |
| `\btau{x}{p}` / `\bepsilon{x}{p}` / `\bvarepsilon{x}{p}` | `\tau x.\, p` / `\epsilon x.\, p` / `\varepsilon x.\, p` | Choice descriptor binders ($\tau \equiv \tau^{\mathrm{Un}}$, $\epsilon \equiv \tau^{\exists!}_{\varnothing}$, $\varepsilon \equiv \tau^{\varnothing}$) |

---

## Compilation

Build sample documents and run validation:

```bash
make
make validate
make test
make clean
```
