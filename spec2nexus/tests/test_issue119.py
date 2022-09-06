"""Test issue 119."""

import os
import sys

from ._core import file_from_tests
from .. import spec

TEST_SPEC_FILE = file_from_tests("issue119_data.txt")
ARGV0 = sys.argv[0]


def test_data_file():
    assert os.path.exists(TEST_SPEC_FILE)

    specData = spec.SpecDataFile(TEST_SPEC_FILE)
    assert isinstance(specData, spec.SpecDataFile)

    scanNum = 1
    scan = specData.getScan(scanNum)
    assert isinstance(scan, spec.SpecDataFileScan)
    assert hasattr(scan.header, "H")

    scan.interpret()
    assert hasattr(scan, "metadata")
    assert "DCM_energy" in scan.metadata
    assert len(scan.metadata) > 15
    assert "DCM_lambda" in scan.metadata


# -----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014-2022, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
