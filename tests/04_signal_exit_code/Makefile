.PHONY: all clean
SHELL=/usr/bin/env bash -eo pipefail

CMD=python3 -c 'import os,signal; os.kill(os.getpid(), signal.SIGKILL)'

all:
	set +e; \
	  ../../galitime/galitime.py --log stdout "$(CMD)" > out.tsv 2> err.txt; \
	  set -e; \
	  ./check_exit_code.py; \
	  grep -q 'Galitime error: non-zero exit code (137)' err.txt

clean:
	rm -f out.tsv err.txt
