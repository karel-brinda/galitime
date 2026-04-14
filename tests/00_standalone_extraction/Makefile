.PHONY: all clean

SHELL=/usr/bin/env bash -eo pipefail

all:
	tmpdir=$$(mktemp -d); \
	trap 'rm -rf "$$tmpdir"' EXIT; \
	cp ../../galitime "$$tmpdir/galitime"; \
	( cd "$$tmpdir" && ./galitime -v | grep -Eq '^galitime [0-9]+(\.[0-9]+)+([A-Za-z0-9._+-]*)$$' )

clean:
