#!/usr/bin/env bash
set -euo pipefail

tmp="$(mktemp)"
python3 ./galitime -h > "$tmp"
export GALITIME_HELP_TMP="$tmp"

python3 - <<'PY'
from pathlib import Path
import re
import os

readme = Path("README.rst")
text = readme.read_text()
help_text = Path(os.environ["GALITIME_HELP_TMP"]).read_text().rstrip()

indented = "\n".join(("    " + line) if line else "" for line in help_text.splitlines())

replacement = f"""CLI
---

.. code-block:: text

{indented}
"""

pattern = r"CLI\n---\n\n\.\. code-block:: text\n.*?(?=\n[A-Z][^\n]*\n[-~`^\"']{3,}\n|\Z)"
new_text, n = re.subn(pattern, replacement, text, flags=re.S)

if n != 1:
    raise SystemExit("Could not uniquely replace CLI block in README.rst")

readme.write_text(new_text)
PY

rm -f "$tmp"
