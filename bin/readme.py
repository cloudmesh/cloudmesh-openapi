# !/usr/bin/env python

import textwrap

from cloudmesh.common.Shell import Shell
from cloudmesh.common.util import readfile
from cloudmesh.common.util import writefile

source = readfile("README-source.md")
icons = readfile("README-icons.md")

manual = Shell.run("cms help openapi")
man = []
start = False
for line in manual.splitlines():
    start = start or "Usage:" in line
    if start:
        if not line.startswith("Timer:"):
            man.append(line)
manual = textwrap.dedent('\n'.join(man)).strip()
manual = "```bash\n" + manual + "\n```\n"

readme = source.format(icons=icons, manual=manual)

writefile("README.md", readme)

print(Shell.cat("README.md"))
