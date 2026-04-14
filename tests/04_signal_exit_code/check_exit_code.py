#!/usr/bin/env python3

import csv
import sys

EXPECTED = '137'
PATH = 'out.tsv'

with open(PATH, newline='') as f:
    rows = list(csv.reader(f, delimiter='\t'))

if len(rows) < 2:
    print('missing data row', file=sys.stderr)
    sys.exit(3)

header = rows[0]
data = rows[1]

try:
    idx = header.index('exit_code')
except ValueError:
    print('missing exit_code column', file=sys.stderr)
    sys.exit(2)

actual = data[idx]
if actual != EXPECTED:
    print(
        f'failed: expected exit_code={EXPECTED} for SIGKILL (128+9), got {actual}',
        file=sys.stderr,
    )
    sys.exit(1)

print(
    f'correct: exit_code={actual}; SIGKILL is reported as shell status 128+9, '
    f'and galitime preserved that value.'
)
