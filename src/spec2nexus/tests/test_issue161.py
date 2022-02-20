"""Test data file with no #E control lines."""

import datetime
import os

from ._core import file_from_tests
from .. import spec


TEST_SPEC_FILE = file_from_tests("issue161_spock_spec_file")


def test_date_and_epoch():
    spec_fmt = "%a %b %d %H:%M:%S %Y"
    assert os.path.exists(TEST_SPEC_FILE)

    specData = spec.SpecDataFile(TEST_SPEC_FILE)
    assert isinstance(specData, spec.SpecDataFile)
    assert hasattr(specData, "headers")
    assert len(specData.headers) == 1
    header = specData.headers[0]
    assert hasattr(header, "date")
    assert hasattr(header, "epoch")
    assert datetime.datetime.strptime(
        header.date, spec_fmt
    ) == datetime.datetime.fromtimestamp(header.epoch), "date and epoch are identical"

    scanNum = 1
    scan = specData.getScan(scanNum)
    assert hasattr(scan, "date")
    assert hasattr(scan, "epoch")
    assert datetime.datetime.strptime(
        scan.date, spec_fmt
    ) == datetime.datetime.fromtimestamp(scan.epoch), "date and epoch are identical"
    assert isinstance(scan, spec.SpecDataFileScan)


# -----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014-2022, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
