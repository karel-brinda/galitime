.PHONY: all clean \
	test_create_venv test_install_package test_installed_version \
	test_installed_stdout_log test_installed_extended_stdout_log \
	test_installed_argv_mode

SHELL := /usr/bin/env bash
.SHELLFLAGS := -eo pipefail -c

PYTHON := /usr/bin/env python3
VENV := $(CURDIR)/_venv
PIP := $(VENV)/bin/python -m pip
GALITIME := $(VENV)/bin/galitime
VERSION_RE := ^galitime [0-9]+(\.[0-9]+)+([A-Za-z0-9._+-]*)$$
EXPECTED_HEADER := experiment	run	real_s	user_s	sys_s	cpu_s	cpu_pct	max_ram_kb	status	exit_code	command
EXPECTED_EXTENDED_HEADER := experiment	run	real_s	user_s	sys_s	cpu_s	cpu_pct	max_ram_kb	backend	fs_inputs	fs_outputs	major_page_faults	minor_page_faults	swaps	status	exit_code	command
CHECK_EXTENDED_COMMAND := /usr/bin/env python3 ../02_simple_tests/check_extended_tsv.py
EXTENDED_BACKEND := gnu
EXTENDED_NOT_NA_ASSERTS := --expect-not-na fs_inputs --expect-not-na fs_outputs --expect-not-na major_page_faults --expect-not-na minor_page_faults --expect-not-na swaps
UNAME_S := $(shell uname -s)

ifeq ($(UNAME_S),Darwin)
EXTENDED_BACKEND := bsd
EXTENDED_NOT_NA_ASSERTS :=
endif

all: test_create_venv test_install_package test_installed_version test_installed_stdout_log test_installed_extended_stdout_log test_installed_argv_mode

test_create_venv:
	@echo "[1/6] Create virtual environment"
	@rm -rf "$(VENV)"
	@$(PYTHON) -m venv "$(VENV)"

test_install_package: test_create_venv
	@echo "[2/6] Install galitime into virtual environment"
	@$(PIP) install ../..

test_installed_version: test_install_package
	@echo "[3/6] Installed CLI version check"
	@$(GALITIME) -v | grep -Eq '$(VERSION_RE)'

test_installed_stdout_log: test_install_package
	@echo "[4/6] Installed CLI stdout logging check"
	@header=$$($(GALITIME) --log stdout "true" | head -n 1); \
	test "$$header" = "$(EXPECTED_HEADER)"

test_installed_extended_stdout_log: test_install_package
	@echo "[5/6] Installed CLI extended logging check"
	@$(GALITIME) -E --log stdout true > out_extended.tsv
	@header=$$(head -n 1 out_extended.tsv); \
	test "$$header" = "$(EXPECTED_EXTENDED_HEADER)"
	@$(CHECK_EXTENDED_COMMAND) out_extended.tsv \
		--expect-header \
		--expect backend=$(EXTENDED_BACKEND) \
		--expect status=ok \
		--expect exit_code=0 \
		--expect command=true \
		$(EXTENDED_NOT_NA_ASSERTS)

test_installed_argv_mode: test_install_package
	@echo "[6/6] Installed CLI argv convenience check"
	@$(GALITIME) --log stdout sleep 0.1 > out.tsv
	@header=$$(head -n 1 out.tsv); \
	test "$$header" = "$(EXPECTED_HEADER)"
	@/usr/bin/env python3 ../02_simple_tests/check_tsv_command.py out.tsv "sleep 0.1"

clean:
	rm -rf "$(VENV)" out.tsv
