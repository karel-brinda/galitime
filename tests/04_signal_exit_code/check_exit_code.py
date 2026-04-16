#!/usr/bin/env python3

import csv
import sys

EXPECTED = '137'
EXPECTED_STATUS = 'failed'
PATH = sys.argv[1] if len(sys.argv) > 1 else 'out.tsv'

with open(PATH, newline='') as f:
    rows = list(csv.reader(f, delimiter='\t'))

if len(rows) < 2:
    print('missing data row', file=sys.stderr)
    sys.exit(3)

header = rows[0]
data = rows[1]

try:
    status_idx = header.index('status')
    exit_code_idx = header.index('exit_code')
except ValueError as err:
    print(f'missing expected column: {err}', file=sys.stderr)
    sys.exit(2)

status = data[status_idx]
if status != EXPECTED_STATUS:
    print(
        f'       failed: expected status={EXPECTED_STATUS}, got {status}',
        file=sys.stderr,
    )
    sys.exit(1)

actual = data[exit_code_idx]
if actual != EXPECTED:
    print(
        f'       failed: expected exit_code={EXPECTED} for SIGKILL (128+9), got {actual}',
        file=sys.stderr,
    )
    sys.exit(1)

print(
    f'       correct: status={status} and exit_code={actual}; SIGKILL is reported as shell status 128+9, and galitime preserved that value.'
)
