# !/usr/bin/env python

import glob
import os
import textwrap

from cloudmesh.common.Shell import Shell
from cloudmesh.common.util import readfile
from cloudmesh.common.util import writefile

#
# Find icons
#

repo = "cloudmesh-openapi"

icons = f"""
[![image](https://img.shields.io/travis/TankerHQ/{repo}.svg?branch=main)](https://travis-ci.org/TankerHQ/{repo})
[![image](https://img.shields.io/pypi/pyversions/{repo}.svg)](https://pypi.org/project/{repo})
[![image](https://img.shields.io/pypi/v/{repo}.svg)](https://pypi.org/project/{repo}/)
[![image](https://img.shields.io/github/license/TankerHQ/python-{repo}.svg)](https://github.com/TankerHQ/python-{repo}/blob/main/LICENSE)
"""

#
# Find Tests
#
tests = glob.glob('tests/test_**.py')
links = [
    "[{name}]({x})".format(x=x, name=os.path.basename(x).replace('.py', '')) for
    x in tests]
tests = " * " + "\n * ".join(links)

#
# get manual
#
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

#
# create readme
#
source = readfile("README-source.md")
readme = source.format(**locals())
writefile("README.md", readme)
