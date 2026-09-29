.DEFAULT_GOAL := paper

PYTHON ?= python3
LATEXMK ?= latexmk
VENV := .venv
VENV_PYTHON := $(VENV)/bin/python
MPLCONFIGDIR := $(CURDIR)/.cache/matplotlib
export MPLCONFIGDIR

.PHONY: all paper figure clean

all: paper

paper: screening.pdf hump.png

figure: hump.pdf hump.png

$(VENV)/.installed: requirements.txt
	$(PYTHON) -m venv $(VENV)
	$(VENV_PYTHON) -m pip install -r requirements.txt
	touch $@

hump.pdf: fig.py $(VENV)/.installed
	$(VENV_PYTHON) fig.py

# fig.py writes both formats. Recover the PNG if it alone was removed.
hump.png: hump.pdf
	@test -f $@ || $(VENV_PYTHON) fig.py

screening.pdf: screening.tex hump.pdf
	$(LATEXMK) -pdf -interaction=nonstopmode -halt-on-error screening.tex

clean:
	$(LATEXMK) -c screening.tex
