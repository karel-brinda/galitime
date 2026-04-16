.PHONY: all clean test_default_backend test_gtime_backend

SHELL := /usr/bin/env bash
.SHELLFLAGS := -eo pipefail -c

GALITIME := ../../galitime
SMALL_MIB := 64
LARGE_MIB := 192
GTIME_AVAILABLE := $(shell command -v gtime >/dev/null 2>&1 && echo yes)

TEST_TARGETS := test_default_backend
TOTAL_STEPS := 1

ifeq ($(GTIME_AVAILABLE),yes)
TEST_TARGETS += test_gtime_backend
TOTAL_STEPS := 2
endif

all: $(TEST_TARGETS)

test_default_backend:
	@echo "[1/$(TOTAL_STEPS)] Default backend memory-unit normalization"
	@$(GALITIME) --log stdout "./alloc_rss.py $(SMALL_MIB)" > default_small.tsv
	@$(GALITIME) --log stdout "./alloc_rss.py $(LARGE_MIB)" > default_large.tsv
	@./check_memory_units.py \
		--small default_small.tsv \
		--large default_large.tsv \
		--small-mib $(SMALL_MIB) \
		--large-mib $(LARGE_MIB) \
		--backend default

test_gtime_backend:
	@echo "[2/$(TOTAL_STEPS)] GNU time memory-unit normalization"
	@$(GALITIME) --gtime --log stdout "./alloc_rss.py $(SMALL_MIB)" > gtime_small.tsv
	@$(GALITIME) --gtime --log stdout "./alloc_rss.py $(LARGE_MIB)" > gtime_large.tsv
	@./check_memory_units.py \
		--small gtime_small.tsv \
		--large gtime_large.tsv \
		--small-mib $(SMALL_MIB) \
		--large-mib $(LARGE_MIB) \
		--backend gtime

clean:
	rm -f default_small.tsv default_large.tsv gtime_small.tsv gtime_large.tsv
