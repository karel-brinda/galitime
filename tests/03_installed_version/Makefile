.PHONY: all clean \
	test_create_venv test_install_package test_installed_version test_installed_stdout_log

SHELL := /usr/bin/env bash
.SHELLFLAGS := -eo pipefail -c

PYTHON := /usr/bin/env python3
VENV := $(CURDIR)/_venv
PIP := $(VENV)/bin/python -m pip
GALITIME := $(VENV)/bin/galitime
VERSION_RE := ^galitime [0-9]+(\.[0-9]+)+([A-Za-z0-9._+-]*)$$
EXPECTED_HEADER := experiment	run	real_s	user_s	sys_s	cpu_s	max_ram_kb	fs_inputs	fs_outputs	exit_code	command

all: test_create_venv test_install_package test_installed_version test_installed_stdout_log

test_create_venv:
	@echo "[1/4] Create virtual environment"
	@rm -rf "$(VENV)"
	@$(PYTHON) -m venv "$(VENV)"

test_install_package: test_create_venv
	@echo "[2/4] Install galitime into virtual environment"
	@$(PIP) install ../..

test_installed_version: test_install_package
	@echo "[3/4] Installed CLI version check"
	@$(GALITIME) -v | grep -Eq '$(VERSION_RE)'

test_installed_stdout_log: test_install_package
	@echo "[4/4] Installed CLI stdout logging check"
	@header=$$($(GALITIME) --log stdout "true" | head -n 1); \
	test "$$header" = "$(EXPECTED_HEADER)"

clean:
	rm -rf "$(VENV)"
