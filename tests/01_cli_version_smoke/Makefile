.PHONY: all clean test_in_tree_version test_copied_version

SHELL := /usr/bin/env bash
.SHELLFLAGS := -eo pipefail -c

GALITIME := ../../galitime
VERSION_RE := ^galitime [0-9]+(\.[0-9]+)+([A-Za-z0-9._+-]*)$$

all: test_in_tree_version test_copied_version

test_in_tree_version:
	@echo "[1/2] In-tree CLI version check"
	@$(GALITIME) -v | grep -Eq '$(VERSION_RE)'

test_copied_version:
	@echo "[2/2] Standalone copied CLI version check"
	@tmpdir=$$(mktemp -d); \
	trap 'rm -rf "$$tmpdir"' EXIT; \
	cp $(GALITIME) "$$tmpdir/galitime"; \
	chmod +x "$$tmpdir/galitime"; \
	( cd "$$tmpdir" && ./galitime -v | grep -Eq '$(VERSION_RE)' )

clean:
