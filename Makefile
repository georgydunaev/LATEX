# Makefile for LaTeX styling package, examples, and validation suite

.PHONY: all compile clean validate test help

PDFLATEX ?= pdflatex
BIBTEX ?= bibtex
PYTHON ?= python3

all: compile

compile:
	@echo "Compiling examples/main.tex..."
	TEXINPUTS="..:.:" $(PDFLATEX) -interaction=nonstopmode -output-directory=examples examples/main.tex
	-cd examples && $(BIBTEX) main
	TEXINPUTS="..:.:" $(PDFLATEX) -interaction=nonstopmode -output-directory=examples examples/main.tex
	TEXINPUTS="..:.:" $(PDFLATEX) -interaction=nonstopmode -output-directory=examples examples/main.tex
	@echo "Compilation completed successfully."

validate:
	$(PYTHON) scripts/validate_latex.py

test:
	$(PYTHON) -m unittest discover -s tests -p 'test_*.py' -v

clean:
	@echo "Cleaning LaTeX build artifacts..."
	rm -f examples/*.aux examples/*.bbl examples/*.blg examples/*.log examples/*.out examples/*.pdf examples/*.toc examples/*.synctex.gz
	rm -f *.aux *.bbl *.blg *.log *.out *.pdf *.toc *.synctex.gz
	rm -rf __pycache__ tests/__pycache__ scripts/__pycache__
	@echo "Clean completed."

help:
	@echo "Available targets:"
	@echo "  all      : Build sample documentation (default)"
	@echo "  compile  : Compile examples/main.tex"
	@echo "  validate : Run macro and document syntax validation script"
	@echo "  test     : Run python unittest test suite"
	@echo "  clean    : Remove generated build artifacts"
