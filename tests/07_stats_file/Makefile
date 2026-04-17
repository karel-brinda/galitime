.PHONY: all clean \
	test_stats_file_ok test_stats_single_run_stddev_na test_stats_failure_partial \
	test_stats_parent_dir_creation test_stats_reject_stdout_stderr_dash

SHELL := /usr/bin/env bash
.SHELLFLAGS := -eo pipefail -c

GALITIME := ../../galitime
UNAME_S := $(shell uname -s)
CHECK_STATS := /usr/bin/env python3 ./check_stats_tsv.py
EXPECTED_LOG_HEADER := experiment	run	real_s	user_s	sys_s	cpu_s	cpu_pct	max_ram_kb	status	exit_code	command

GALITIME_RUN := $(GALITIME)
ifeq ($(UNAME_S),Darwin)
GALITIME_RUN := $(GALITIME) --gtime
endif

all: \
	test_stats_file_ok \
	test_stats_single_run_stddev_na \
	test_stats_failure_partial \
	test_stats_parent_dir_creation \
	test_stats_reject_stdout_stderr_dash

test_stats_file_ok:
	@echo "[1/5] Stats file for successful repeated run"
	@$(GALITIME_RUN) -r 5 --log runs.log --stats stats.tsv sleep 0.1
	@awk -F '\t' '\
		NR == 1 { \
			if ($$0 != "$(EXPECTED_LOG_HEADER)") { \
				print "ERROR: unexpected log header: " $$0; \
				exit 1; \
			} \
			next; \
		} \
		END { \
			if (NR != 6) { \
				print "ERROR: expected 6 lines in runs.log, got " NR; \
				exit 1; \
			} \
		}' runs.log
	@$(CHECK_STATS) stats.tsv --expect-header \
		--expect runs_requested=5 \
		--expect runs_completed=5 \
		--expect runs_summarized=5 \
		--expect runs_ok=5 \
		--expect runs_failed=0 \
		--expect runs_timeout=0 \
		--expect runs_timing_error=0 \
		--expect final_status=ok \
		--expect final_exit_code=0 \
		--expect "command=sleep 0.1"

test_stats_single_run_stddev_na:
	@echo "[2/5] Single successful run reports NA stddev"
	@$(GALITIME_RUN) -r 1 --stats stats_single.tsv true >/dev/null 2>/dev/null
	@$(CHECK_STATS) stats_single.tsv \
		--expect runs_summarized=1 \
		--all-stddev-na

test_stats_failure_partial:
	@echo "[3/5] Failed command still writes partial stats"
	@set +e; \
	$(GALITIME_RUN) -r 5 --stats stats_fail.tsv false >/dev/null 2> stats_fail.err; \
	status=$$?; \
	set -e; \
	[[ "$$status" -ne 0 ]] || { \
		echo "ERROR: expected non-zero exit status for false"; \
		exit 1; \
	}; \
	test -f stats_fail.tsv
	@$(CHECK_STATS) stats_fail.tsv \
		--expect runs_requested=5 \
		--expect runs_completed=1 \
		--expect runs_summarized=0 \
		--expect runs_ok=0 \
		--expect runs_failed=1 \
		--expect final_status=failed \
		--expect final_exit_code=1 \
		--all-numeric-na

test_stats_parent_dir_creation:
	@echo "[4/5] Stats parent directories are created"
	@$(GALITIME_RUN) --stats nested/dir/stats.tsv true >/dev/null 2>/dev/null
	@test -f nested/dir/stats.tsv

test_stats_reject_stdout_stderr_dash:
	@echo "[5/5] Stats rejects stream-like destinations"
	@for value in stdout stderr -; do \
		set +e; \
		$(GALITIME) --stats "$$value" true > "reject_$$value.out" 2> "reject_$$value.err"; \
		status=$$?; \
		set -e; \
		[[ "$$status" -ne 0 ]] || { \
			echo "ERROR: expected non-zero exit status for --stats $$value"; \
			exit 1; \
		}; \
		grep -q 'real file path' "reject_$$value.err"; \
	done

clean:
	rm -f runs.log stats.tsv stats_single.tsv stats_fail.tsv stats_fail.err
	rm -f reject_stdout.out reject_stdout.err reject_stderr.out reject_stderr.err
	rm -f reject_-.out reject_-.err
	rm -rf nested
