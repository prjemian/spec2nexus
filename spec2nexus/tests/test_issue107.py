"""Test issues 107 and 133."""

import h5py
import os

from ._core import hfile
from ._core import file_from_tests
from .. import spec
from .. import writer


TEST_SPEC_FILE = file_from_tests("JL124_1.spc")


def test_issue107_data_file():
    assert os.path.exists(TEST_SPEC_FILE)

    sdf = spec.SpecDataFile(TEST_SPEC_FILE)
    assert isinstance(sdf, spec.SpecDataFile)

    scanNum = 4
    scan = sdf.getScan(scanNum)
    assert isinstance(scan, spec.SpecDataFileScan)
    assert hasattr(scan.header, "H")
    assert hasattr(scan, "V")

    scan.interpret()
    assert hasattr(scan, "metadata")
    assert len(scan.metadata) == 140


def test_issue133_data_file(hfile):
    assert os.path.exists(TEST_SPEC_FILE)

    sdf = spec.SpecDataFile(TEST_SPEC_FILE)
    scanNum = 1
    scan = sdf.getScan(scanNum)
    assert isinstance(scan, spec.SpecDataFileScan)

    # issue #137 & #140
    try:
        u = scan.__getattribute__("U")
    except AttributeError:
        u = None
    assert u is not None, "U attribute lazy loaded"
    # not needed: scan.interpret()
    assert hasattr(scan, "U"), "#U in scan #1"
    assert len(scan.U) == 1, "only one #U in scan #1"

    assert hasattr(scan.header, "U"), "#U in scan header"
    assert len(scan.header.U) == 1, "only one #U in header"

    # test for UserReserved in a NeXus file

    specwriter = writer.Writer(sdf)
    specwriter.save(hfile, "1 2 3 4 5".split())
    assert os.path.exists(hfile)

    with h5py.File(hfile, "r") as fp:
        entry = fp.get("/S1")
        assert entry is not None, "group /S1"

        u = entry.get("UserReserved")
        assert u is not None, "group /S1/UserReserved"
        assert u.get("header_1") is not None, "dataset /S1/UserReserved/header_1"
        assert u.get("header_2") is None, "dataset /S1/UserReserved/header_2"
        assert u.get("item_1") is not None, "dataset /S1/UserReserved/item_1"
        assert u.get("item_2") is None, "dataset /S1/UserReserved/item_2"

        entry = fp.get("/S2")
        assert entry is not None, "group /S2"

        u = entry.get("UserReserved")
        assert u is not None, "group /S2/UserReserved"
        assert u.get("header_1") is not None, "dataset /S1/UserReserved/header_1"
        assert u.get("header_2") is None, "dataset /S1/UserReserved/header_2"
        assert u.get("item_1") is None, "dataset /S1/UserReserved/item_1"
        assert u.get("item_2") is None, "dataset /S1/UserReserved/item_2"


# -----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014-2022, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
