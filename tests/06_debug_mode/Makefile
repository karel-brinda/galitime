.PHONY: all clean test_debug_stdout_log test_quiet_stdout_log

SHELL := /usr/bin/env bash
.SHELLFLAGS := -eo pipefail -c

GALITIME := ../../galitime
TOTAL_STEPS := 2

all: test_debug_stdout_log test_quiet_stdout_log

test_debug_stdout_log:
	@echo "[1/$(TOTAL_STEPS)] Debug stderr trace with stdout log"
	@$(GALITIME) --debug --log stdout true > out.tsv 2> err.log
	@grep -q '^experiment' out.tsv
	@grep -q '\[galitime ' err.log
	@grep -q 'starting' err.log
	@grep -q 'backend:' err.log
	@grep -q 'wrapped command:' err.log
	@grep -q 'final exit code: 0' err.log

test_quiet_stdout_log:
	@echo "[2/$(TOTAL_STEPS)] No debug trace without --debug"
	@$(GALITIME) --log stdout true > out_quiet.tsv 2> err_quiet.log
	@grep -q '^experiment' out_quiet.tsv
	@! grep -q '\[galitime ' err_quiet.log
	@! grep -q 'wrapped command:' err_quiet.log

clean:
	rm -f out.tsv err.log out_quiet.tsv err_quiet.log
