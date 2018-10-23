
"""
use source code debugger to identify and resolve sphinx-build problems
"""

import os
import re
import sys

from sphinx.cmd import build

# from Makefile
# sphinx-build -b html -d $(BUILDDIR)/doctrees $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) source  $(BUILDDIR)/html

def main():
    options = """
    -b html -d {builddir}/doctrees {paperopt} {sphinxopts} source  {builddir}/html
    """.format(
        builddir=os.getcwd(),
        paperopt="-D latex_paper_size=letter",
        sphinxopts="",
        ).strip()
    
    build.main(options.split())


if __name__ == "__main__":
    main()
