"""Test issue 188."""

import os
import sys

from . import _core
from .. import spec


TEST_SPEC_FILE = os.path.join(_core.EXAMPLES_PATH, "startup_1.spec")

# class Issue188(unittest.TestCase):
#     def setUp(self):
#         TEST_SPEC_FILE = os.path.join(
#             _path, "spec2nexus", "data", "startup_1.spec"
#         )
#         self.sys_argv0 = sys.argv[0]

#     def tearDown(self):
#         sys.argv = [
#             self.sys_argv0,
#         ]


def test_scan_unrecognized():
    assert os.path.exists(TEST_SPEC_FILE)

    sdf = spec.SpecDataFile(TEST_SPEC_FILE)
    assert isinstance(sdf, spec.SpecDataFile)

    scanNum = 16
    scan = sdf.getScan(scanNum)
    scan.interpret()

    assert hasattr(scan, "data")
    assert hasattr(scan, "_unrecognized")
    assert len(scan._unrecognized) == 112


def test_data_file():
    assert os.path.exists(TEST_SPEC_FILE)

    sdf = spec.SpecDataFile(TEST_SPEC_FILE)
    assert isinstance(sdf, spec.SpecDataFile)

    for scanNum in sdf.getScanNumbers():
        scan = sdf.getScan(scanNum)
        assert isinstance(scan, spec.SpecDataFileScan)
        assert hasattr(scan, "L")
        assert isinstance(scan.L, list)
        assert hasattr(scan, "N")
        assert isinstance(scan.N, list)
        assert len(scan.N) >= 1
        assert len(scan.L) == scan.N[0], "scan %s #L line" % scanNum

        assert hasattr(scan, "data")
        assert isinstance(scan.data, dict)

        n = len(scan.data.keys())
        if n > 0:  # if ==0, then no data present
            assert len(scan.L) == n, "scan %s #L line" % scanNum


# -----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014-2022, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
