.PHONY: all help mac clean

SHELL := /usr/bin/env bash -eo pipefail

.SECONDARY:
.SUFFIXES:

##############
## Commands ##
##############

all: ## Run standard smoke tests; run mac-specific gtime test on Darwin
	@echo "[1/4] Basic logging test"
	../../galitime --log time.log ls
	@echo "[2/4] Stdout redirection smoke test"
	((../../galitime ls >/dev/null) 2>&1) > time2.log
	@echo "[3/4] Repeated run smoke test"
	../../galitime -r 5 --log time3.log "sleep 0.1"
	@if [[ "$$(uname)" == "Darwin" ]]; then \
		echo "[4/4] Running macOS-specific tests"; \
		$(MAKE) mac; \
	else \
		echo "[4/4] Skipping macOS-specific tests on non-Darwin"; \
	fi

mac: ## Run macOS-specific test for --gtime
	@echo "Checking that gtime is available"
	@command -v gtime >/dev/null || { \
		echo "ERROR: gtime not found in PATH"; \
		echo "Install it with: brew install gnu-time"; \
		exit 1; \
	}
	@echo "Running galitime with --gtime"
	../../galitime --gtime --log time_gtime.log "true"
	@echo "Checking that the log file is not empty"
	@test -s time_gtime.log || { \
		echo "ERROR: time_gtime.log was not created or is empty"; \
		exit 1; \
	}
	@echo "Checking that the header starts with 'experiment'"
	@grep -q '^experiment' time_gtime.log || { \
		echo "ERROR: expected header starting with 'experiment' in time_gtime.log"; \
		echo "Actual contents:"; \
		cat time_gtime.log; \
		exit 1; \
	}
	@echo "Checking that the command completed successfully"
	@tail -n 1 time_gtime.log | grep -q "$$(printf '\t0\ttrue$$')" || { \
		echo "ERROR: expected a successful run ending with tab-0-tab-true"; \
		echo "Actual contents:"; \
		cat time_gtime.log; \
		exit 1; \
	}
	@echo "macOS gtime test passed"

help: ## Print help messages
	@echo -e "$$(grep -hE '^\S*(:.*)?##' $(MAKEFILE_LIST) \
		| sed \
			-e 's/:.*##\s*/:/' \
			-e 's/^\(.*\):\(.*\)/   \\x1b[36m\1\\x1b[m:\2/' \
			-e 's/^\([^#]\)/\1/g' \
			-e 's/: /:/g' \
			-e 's/^#\(.*\)#/\\x1b[90m\1\\x1b[m/' \
		| column -c2 -t -s : )"

clean: ## Clean
	rm -f *.log
