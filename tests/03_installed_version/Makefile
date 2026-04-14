.PHONY: all clean

PYTHON := /usr/bin/env python3
VENV := $(CURDIR)/_venv

all:
	rm -rf "$(VENV)"
	$(PYTHON) -m venv "$(VENV)"
	$(VENV)/bin/python -m pip install ../..
	$(VENV)/bin/galitime -v | grep -Eq '^galitime [0-9]+(\.[0-9]+)+([A-Za-z0-9._+-]*)$$'
	$(VENV)/bin/galitime --log stdout "true" | grep -q '^experiment'

clean:
	rm -rf "$(VENV)"
