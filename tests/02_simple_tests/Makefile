.PHONY: all clean \
	test_file_log test_stderr_default test_stdout_log test_repeat \
	test_argv_sleep test_argv_double_dash test_single_string_mode \
	test_space_argument test_hyphen_argument test_quoted_shell_expression \
	test_literal_metacharacters test_unknown_option_error \
	test_gtime_stdout_log test_gtime_file_log

SHELL := /usr/bin/env bash
.SHELLFLAGS := -eo pipefail -c

GALITIME := ../../galitime
UNAME_S := $(shell uname -s)

BASE_TARGETS := \
	test_file_log \
	test_stderr_default \
	test_stdout_log \
	test_repeat \
	test_argv_sleep \
	test_argv_double_dash \
	test_single_string_mode \
	test_space_argument \
	test_hyphen_argument \
	test_quoted_shell_expression \
	test_literal_metacharacters \
	test_unknown_option_error
TOTAL_STEPS := 12
EXPECTED_HEADER := experiment	run	real_s	user_s	sys_s	cpu_s	cpu_pct	max_ram_kb	status	exit_code	command
CHECK_COMMAND := /usr/bin/env python3 ./check_tsv_command.py

ifeq ($(UNAME_S),Darwin)
BASE_TARGETS += test_gtime_stdout_log test_gtime_file_log
TOTAL_STEPS := 14
endif

all: $(BASE_TARGETS)

define ASSERT_TSV_OK
	@test -s "$(1)" || { \
		echo "ERROR: $(1) is missing or empty"; \
		exit 1; \
	}
	@awk -F '\t' '\
		NR == 1 { \
			if ($$0 != "$(EXPECTED_HEADER)") { \
				print "ERROR: unexpected header in $(1): " $$0; \
				exit 1; \
			} \
			for (i = 1; i <= NF; i++) if ($$i == "status") st = i; \
			for (i = 1; i <= NF; i++) if ($$i == "exit_code") ec = i; \
			if (!st || !ec) { \
				print "ERROR: missing status or exit_code column in $(1)"; \
				exit 1; \
			} \
			next; \
		} \
		NR > 1 { \
			if ($$st != "ok") { \
				print "ERROR: unexpected status in $(1): " $$0; \
				exit 1; \
			} \
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

define ASSERT_GTIME_AVAILABLE
	@command -v gtime >/dev/null || { \
		echo "ERROR: gtime not found in PATH"; \
		echo "Install it with: brew install gnu-time"; \
		exit 1; \
	}
endef

test_file_log:
	@echo "[1/$(TOTAL_STEPS)] File log test"
	@$(GALITIME) --log time.log true
	$(call ASSERT_TSV_OK,time.log)

test_stderr_default:
	@echo "[2/$(TOTAL_STEPS)] Default stderr log test"
	@$(GALITIME) "echo ok" >/dev/null 2> time2.log
	$(call ASSERT_TSV_OK,time2.log)

test_stdout_log:
	@echo "[3/$(TOTAL_STEPS)] Explicit stdout log test"
	@$(GALITIME) --log stdout true > time_stdout.log
	$(call ASSERT_TSV_OK,time_stdout.log)

test_repeat:
	@echo "[4/$(TOTAL_STEPS)] Repeated-run test"
	@$(GALITIME) -r 5 --log time3.log "sleep 0.1"
	$(call ASSERT_TSV_OK,time3.log)
	@awk 'END { if (NR != 6) { print "ERROR: expected 6 lines in time3.log, got " NR; exit 1 } }' time3.log

test_argv_sleep:
	@echo "[5/$(TOTAL_STEPS)] Argv convenience mode test"
	@$(GALITIME) --log time_argv.log sleep 0.1
	$(call ASSERT_TSV_OK,time_argv.log)
	@$(CHECK_COMMAND) time_argv.log "sleep 0.1"

test_argv_double_dash:
	@echo "[6/$(TOTAL_STEPS)] Explicit -- command tail test"
	@$(GALITIME) --log time_double_dash.log -- sleep 0.1
	$(call ASSERT_TSV_OK,time_double_dash.log)
	@$(CHECK_COMMAND) time_double_dash.log "sleep 0.1"

test_single_string_mode:
	@echo "[7/$(TOTAL_STEPS)] Raw shell-command single-string test"
	@$(GALITIME) --log time_single_string.log "printf '%s\n' single-string > single_string.out"
	$(call ASSERT_TSV_OK,time_single_string.log)
	@$(CHECK_COMMAND) time_single_string.log "printf '%s\n' single-string > single_string.out"
	@test "$$(cat single_string.out)" = "single-string"

test_space_argument:
	@echo "[8/$(TOTAL_STEPS)] Space-containing argument test"
	@$(GALITIME) --log time_space_argument.log printf '%s\n' "hello world" > space_argument.out
	$(call ASSERT_TSV_OK,time_space_argument.log)
	@$(CHECK_COMMAND) time_space_argument.log "printf '%s\n' 'hello world'"
	@test "$$(cat space_argument.out)" = "hello world"

test_hyphen_argument:
	@echo "[9/$(TOTAL_STEPS)] Hyphen-prefixed argument test"
	@$(GALITIME) --log time_hyphen_argument.log python3 -c "import sys; print(sys.argv[1])" -n > hyphen_argument.out
	$(call ASSERT_TSV_OK,time_hyphen_argument.log)
	@$(CHECK_COMMAND) time_hyphen_argument.log "python3 -c 'import sys; print(sys.argv[1])' -n"
	@test "$$(cat hyphen_argument.out)" = "-n"

test_quoted_shell_expression:
	@echo "[10/$(TOTAL_STEPS)] Quoted shell-expression test"
	@$(GALITIME) --log time_quoted_shell_expression.log "printf 'a\n' && printf 'b\n'" > quoted_shell_expression.out
	$(call ASSERT_TSV_OK,time_quoted_shell_expression.log)
	@$(CHECK_COMMAND) time_quoted_shell_expression.log "printf 'a\n' && printf 'b\n'"
	@printf 'a\nb\n' > quoted_shell_expression.expected
	@cmp -s quoted_shell_expression.expected quoted_shell_expression.out || { \
		echo "ERROR: quoted shell expression did not preserve shell semantics"; \
		exit 1; \
	}

test_literal_metacharacters:
	@echo "[11/$(TOTAL_STEPS)] Literal shell metacharacter test"
	@$(GALITIME) --log time_literal_metacharacters.log printf '%s\n' ">" "|" "&&" ";" "*.txt" '$$(printf hi)' > literal_metacharacters.out
	$(call ASSERT_TSV_OK,time_literal_metacharacters.log)
	@$(CHECK_COMMAND) time_literal_metacharacters.log "printf '%s\n' '>' '|' '&&' ';' '*.txt' '\$$(printf hi)'"
	@printf '%s\n' '>' '|' '&&' ';' '*.txt' '$$(printf hi)' > literal_metacharacters.expected
	@cmp -s literal_metacharacters.expected literal_metacharacters.out || { \
		echo "ERROR: literal metacharacter arguments were not preserved"; \
		exit 1; \
	}

test_unknown_option_error:
	@echo "[12/$(TOTAL_STEPS)] Unknown galitime option error test"
	@! $(GALITIME) -x true > unknown_option.out 2> unknown_option.err
	@grep -q 'unrecognized arguments: -x' unknown_option.err
	@test ! -s unknown_option.out

test_gtime_stdout_log:
	@echo "[13/$(TOTAL_STEPS)] macOS GNU time stdout log test"
	$(call ASSERT_GTIME_AVAILABLE)
	@$(GALITIME) --gtime --log stdout true > time_gtime_stdout.log
	$(call ASSERT_TSV_OK,time_gtime_stdout.log)

test_gtime_file_log:
	@echo "[14/$(TOTAL_STEPS)] macOS GNU time file log test"
	$(call ASSERT_GTIME_AVAILABLE)
	@$(GALITIME) --gtime --log time_gtime.log true
	$(call ASSERT_TSV_OK,time_gtime.log)

clean:
	rm -f *.log *.out *.err *.expected
