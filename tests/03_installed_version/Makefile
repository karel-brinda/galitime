.PHONY: all clean \
	test_create_venv test_install_package test_installed_version \
	test_installed_stdout_log test_installed_argv_mode

SHELL := /usr/bin/env bash
.SHELLFLAGS := -eo pipefail -c

PYTHON := /usr/bin/env python3
VENV := $(CURDIR)/_venv
PIP := $(VENV)/bin/python -m pip
GALITIME := $(VENV)/bin/galitime
VERSION_RE := ^galitime [0-9]+(\.[0-9]+)+([A-Za-z0-9._+-]*)$$
EXPECTED_HEADER := experiment	run	real_s	user_s	sys_s	cpu_s	cpu_pct	max_ram_kb	status	exit_code	command

all: test_create_venv test_install_package test_installed_version test_installed_stdout_log test_installed_argv_mode

test_create_venv:
	@echo "[1/5] Create virtual environment"
	@rm -rf "$(VENV)"
	@$(PYTHON) -m venv "$(VENV)"

test_install_package: test_create_venv
	@echo "[2/5] Install galitime into virtual environment"
	@$(PIP) install ../..

test_installed_version: test_install_package
	@echo "[3/5] Installed CLI version check"
	@$(GALITIME) -v | grep -Eq '$(VERSION_RE)'

test_installed_stdout_log: test_install_package
	@echo "[4/5] Installed CLI stdout logging check"
	@header=$$($(GALITIME) --log stdout "true" | head -n 1); \
	test "$$header" = "$(EXPECTED_HEADER)"

test_installed_argv_mode: test_install_package
	@echo "[5/5] Installed CLI argv convenience check"
	@$(GALITIME) --log stdout sleep 0.1 > out.tsv
	@header=$$(head -n 1 out.tsv); \
	test "$$header" = "$(EXPECTED_HEADER)"
	@/usr/bin/env python3 ../02_simple_tests/check_tsv_command.py out.tsv "sleep 0.1"

clean:
	rm -rf "$(VENV)" out.tsv
