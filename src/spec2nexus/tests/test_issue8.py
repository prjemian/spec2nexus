"""Test issue 8."""

# -----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014-2020, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------

import os

from ._core import TEST_DATA_DIR
from .. import spec


TEST_FILE = os.path.join(TEST_DATA_DIR, "n_m.txt")


def test_data_file():
    assert os.path.exists(TEST_FILE)

    specData = spec.SpecDataFile(TEST_FILE)
    assert isinstance(specData, spec.SpecDataFile)

    scanNum = 6
    scan = specData.getScan(scanNum)
    assert scan is not None
    assert isinstance(scan, spec.SpecDataFileScan)
    assert hasattr(scan, "data")
    assert isinstance(scan.data, dict)
    assert "mr" in scan.data
    assert len(scan.data["mr"]) == 31
    assert not hasattr(scan, "_mca_")