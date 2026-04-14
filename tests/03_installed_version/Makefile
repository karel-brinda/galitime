.PHONY: all clean

PYTHON=/usr/bin/env python
VENV=$(CURDIR)/_venv

all:
	$(PYTHON) -m venv "$(VENV)"
	$(VENV)/bin/pip install ../..
	$(VENV)/bin/galitime -v | grep -Eq '^galitime [0-9]+(\.[0-9]+)+([A-Za-z0-9._+-]*)$$'

clean:
	rm -rf "$(VENV)"
