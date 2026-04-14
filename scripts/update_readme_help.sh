#!/usr/bin/env bash
set -euo pipefail

HELP_FILE="$(mktemp)"
python3 ./galitime -h > "$HELP_FILE"

python3 - <<'PY'
from pathlib import Path
import re
import os

readme = Path("README.rst")
text = readme.read_text()

help_text = Path(os.environ["HELP_FILE"]).read_text().rstrip()

replacement = (
    "CLI\n"
    "---\n\n"
    ".. code-block:: text\n\n"
    + "\n".join(f"    {line}" if line else "" for line in help_text.splitlines())
    + "\n"
)

pattern = r"CLI\n---\n\n\.\. code-block:: text\n.*?(?=\n[A-Z][^\n]*\n[-~`^\"']{3,}\n|\Z)"
new_text, n = re.subn(pattern, replacement, text, flags=re.S)

if n != 1:
    raise SystemExit("Could not uniquely replace CLI block in README.rst")

readme.write_text(new_text)
PY
