.PHONY: all help clean cleanall view

SHELL=/usr/bin/env bash -eo pipefail

.SECONDARY:

.SUFFIXES:

##############
## Commands ##
##############

all:
	../../galitime/galitime.py --log time.log ls
	((../../galitime/galitime.py ls >/dev/null) 2>&1) > time2.log

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

cleanall: clean ## Clean all

view: ## View output
