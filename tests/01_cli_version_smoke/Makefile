.PHONY: all clean

SHELL := /usr/bin/env bash
.SHELLFLAGS := -eo pipefail -c

all:
	@echo "[1/2] In-tree CLI version check"
	@../../galitime -v | grep -Eq '^galitime [0-9]+(\.[0-9]+)+([A-Za-z0-9._+-]*)$$'

	@echo "[2/2] Standalone copied CLI version check"
	@tmpdir=$$(mktemp -d); \
	trap 'rm -rf "$$tmpdir"' EXIT; \
	cp ../../galitime "$$tmpdir/galitime"; \
	chmod +x "$$tmpdir/galitime"; \
	( cd "$$tmpdir" && ./galitime -v | grep -Eq '^galitime [0-9]+(\.[0-9]+)+([A-Za-z0-9._+-]*)$$' )

clean:
