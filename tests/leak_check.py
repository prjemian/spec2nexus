#!/usr/bin/env python

"""
try to provoke the memory leak described

https://github.com/prjemian/spec2nexus/issues/127

file: /Users/hammonds/RSM_DATA/DanielHaskel/Brian-Nick/Fluorescence/lineup
We don't have that one.
"""


import gc
import os
import resource
from spec2nexus.spec import SpecDataFile
import sys
import time

_path = os.path.dirname(__file__)
# TESTFILE = "tests/data/issue119_data.txt"
TESTFILE = os.path.join(_path, "data", "issue119_data.txt")

t0 = time.time()


def get_memory():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0


def task():
    gc.collect()
    before = get_memory()
    # gc.set_debug(gc.DEBUG_LEAK)
    a = SpecDataFile(TESTFILE)
    after = get_memory()
    a = None
    gc.collect()
    final = get_memory()

    d = dict(
        time=time.time() - t0,
        before=before,
        after=after,
        final=final,
    )

    print(f"{d}")


if __name__ == "__main__":
    while True:
        task()
        time.sleep(1.0)
