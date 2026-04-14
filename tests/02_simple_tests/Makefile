.PHONY: all clean test_file_log test_stderr_default test_stdout_log test_repeat mac

SHELL := /usr/bin/env bash
.SHELLFLAGS := -eo pipefail -c

GALITIME := ../../galitime
UNAME_S := $(shell uname -s)

ALL_TARGETS := test_file_log test_stderr_default test_stdout_log test_repeat
ifeq ($(UNAME_S),Darwin)
ALL_TARGETS += mac
endif

all: $(ALL_TARGETS)

define ASSERT_TSV_OK
	@test -s "$(1)" || { \
		echo "ERROR: $(1) is missing or empty"; \
		exit 1; \
	}
	@awk -F '\t' '\
		NR == 1 { \
			if ($$1 != "experiment") { \
				print "ERROR: first column is not experiment in $(1)"; \
				exit 1; \
			} \
			for (i = 1; i <= NF; i++) if ($$i == "exit_code") ec = i; \
			if (!ec) { \
				print "ERROR: missing exit_code column in $(1)"; \
				exit 1; \
			} \
			next; \
		} \
		NR > 1 { \
			if ($$ec != 0) { \
				print "ERROR: non-zero exit_code in $(1): " $$0; \
				exit 1; \
			} \
			rows++; \
		} \
		END { \
			if (rows < 1) { \
				print "ERROR: no data rows in $(1)"; \
				exit 1; \
			} \
		}' "$(1)"
endef

test_file_log:
	@echo "Running file log test"
	@$(GALITIME) --log time.log true
	$(call ASSERT_TSV_OK,time.log)

test_stderr_default:
	@echo "Running default stderr log test"
	@$(GALITIME) "echo ok" >/dev/null 2> time2.log
	$(call ASSERT_TSV_OK,time2.log)

test_stdout_log:
	@echo "Running explicit stdout log test"
	@$(GALITIME) --log stdout true > time_stdout.log
	$(call ASSERT_TSV_OK,time_stdout.log)

test_repeat:
	@echo "Running repeated-run test"
	@$(GALITIME) -r 5 --log time3.log "sleep 0.1"
	$(call ASSERT_TSV_OK,time3.log)
	@awk 'END { if (NR != 6) { print "ERROR: expected 6 lines in time3.log, got " NR; exit 1 } }' time3.log

mac:
	@echo "Running macOS gtime tests"
	@command -v gtime >/dev/null || { \
		echo "ERROR: gtime not found in PATH"; \
		echo "Install it with: brew install gnu-time"; \
		exit 1; \
	}
	@$(GALITIME) --gtime --log stdout true > time_gtime_stdout.log
	$(call ASSERT_TSV_OK,time_gtime_stdout.log)
	@$(GALITIME) --gtime --log time_gtime.log true
	$(call ASSERT_TSV_OK,time_gtime.log)

clean:
	rm -f *.log
