.PHONY: all help mac clean

SHELL=/usr/bin/env bash -eo pipefail

.SECONDARY:

.SUFFIXES:

##############
## Commands ##
##############

all:
	../../galitime --log time.log ls
	((../../galitime ls >/dev/null) 2>&1) > time2.log
	../../galitime -r 5 --log time3.log "sleep 0.1"
	@if [[ "$$(uname)" == "Darwin" ]]; then \
		$(MAKE) mac; \
	fi

mac:
	@command -v gtime >/dev/null
	../../galitime --gtime --log time_gtime.log "true"
	@grep -q '^experiment$$' time_gtime.log'
	@grep -q $'\t0\ttrue$$' time_gtime.log


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
