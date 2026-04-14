.DEFAULT_GOAL := help

.PHONY: \
	all clean install build \
	test \
	pylint flake8 format \
	help

PYTHON ?= python3

#################
## BASIC RULES ##
#################

all: help

help: ## Print help messages
	@printf '%b\n' "$$(grep -hE '^\S*(:.*)?##|^#.*#$$' $(MAKEFILE_LIST) \
		| sed \
			-e '/:/ s/[[:space:]]*##[[:space:]]*/ /' \
			-e 's/^\(.*\):\(.*\)/   \\x1b[36m\1\\x1b[m:\2/' \
			-e 's/^\([^#]\)/\1/g' \
			-e 's/: /:/g' \
			-e 's/^#\(.*\)#/\\x1b[90m\1\\x1b[m/' \
		| column -c2 -t -s : )"

clean: ## Clean build artifacts and test outputs
	rm -rf build dist *.egg-info
	$(MAKE) -C tests clean

install: ## Install using python -m pip
	$(PYTHON) -m pip install .

build: ## Build sdist and wheel
	$(PYTHON) -m build


#############
## TESTING ##
#############

test: ## Run tests
	$(MAKE) -C tests clean
	$(MAKE) -C tests

pylint: ## Run PyLint
	$(PYTHON) -m pylint galitime

flake8: ## Run Flake8
	flake8 galitime tests

format: ## Run YAPF (inline replacement)
	yapf -i --recursive galitime tests
