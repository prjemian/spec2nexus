"""Test for multiple headers."""

import os
import pytest
import sys

from .. import spec
from . import _core

TESTFILE = os.path.join(_core.EXAMPLES_PATH, "05_02_test.dat")
ARGV0 = sys.argv[0]


def test_data_file():
    assert os.path.exists(TESTFILE)

    # with pytest.raises(spec.DuplicateSpecScanNumber) as exc:
    #     specData = spec.SpecDataFile(TESTFILE)

    # should not raise an exception
    specData = spec.SpecDataFile(TESTFILE)
    assert isinstance(specData, spec.SpecDataFile)

    scanNum = 110
    scan = specData.getScan(scanNum)
    assert isinstance(scan, spec.SpecDataFileScan)

    scanNum = 1.17
    scan = specData.getScan(scanNum)
    assert isinstance(scan, spec.SpecDataFileScan)
    raw = scan.raw.splitlines()
    assert raw[0].startswith("#S 1 ")
    assert isinstance(scan.scanNum, str)
    assert scan.scanNum == "1.17"


# -----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014-2022, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
