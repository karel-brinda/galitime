#! /usr/bin/env python3

import re
import sys
from pathlib import Path

vfn = Path(__file__).with_name("galitime.py")

content = vfn.read_text(encoding="utf-8")
match = re.search(r'^__version__\s*=\s*"([^"]+)"', content, re.MULTILINE)
if not match:
    raise RuntimeError("Unable to find __version__ in galitime.py")

numbers = match.group(1).split(".")
numbers[-1] = str(int(numbers[-1]) + 1)

version = ".".join(numbers)

updated = re.sub(
    r'^__version__\s*=\s*"([^"]+)"',
    '__version__ = "{}"'.format(version),
    content,
    count=1,
    flags=re.MULTILINE,
)
vfn.write_text(updated, encoding="utf-8")
