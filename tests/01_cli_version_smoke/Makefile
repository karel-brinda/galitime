.PHONY: all clean test_in_tree_version test_copied_version test_copied_argv_mode

SHELL := /usr/bin/env bash
.SHELLFLAGS := -eo pipefail -c

GALITIME := ../../galitime
VERSION_RE := ^galitime [0-9]+(\.[0-9]+)+([A-Za-z0-9._+-]*)$$

all: test_in_tree_version test_copied_version test_copied_argv_mode

test_in_tree_version:
	@echo "[1/3] In-tree CLI version check"
	@$(GALITIME) -v | grep -Eq '$(VERSION_RE)'

test_copied_version:
	@echo "[2/3] Standalone copied CLI version check"
	@tmpdir=$$(mktemp -d); \
	trap 'rm -rf "$$tmpdir"' EXIT; \
	cp $(GALITIME) "$$tmpdir/galitime"; \
	chmod +x "$$tmpdir/galitime"; \
	( cd "$$tmpdir" && ./galitime -v | grep -Eq '$(VERSION_RE)' )

test_copied_argv_mode:
	@echo "[3/3] Standalone copied CLI argv convenience check"
	@tmpdir=$$(mktemp -d); \
	trap 'rm -rf "$$tmpdir"' EXIT; \
	cp $(GALITIME) "$$tmpdir/galitime"; \
	chmod +x "$$tmpdir/galitime"; \
	( cd "$$tmpdir" && ./galitime --log stdout sleep 0.1 > out.tsv ); \
	/usr/bin/env python3 ../02_simple_tests/check_tsv_command.py "$$tmpdir/out.tsv" "sleep 0.1"

clean:
