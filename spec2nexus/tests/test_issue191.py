"""Test issue 191."""

import h5py
import os

from ._core import file_from_tests
from ._core import testpath
from .. import spec
from .. import writer

TEST_SPEC_FILE = file_from_tests("JL124_1.spc")


def test_nexus_file(testpath):
    assert os.path.exists(TEST_SPEC_FILE)

    sdf = spec.SpecDataFile(TEST_SPEC_FILE)
    assert isinstance(sdf, spec.SpecDataFile)

    scanNum = 1
    scan = sdf.getScan(scanNum)
    assert isinstance(scan, spec.SpecDataFileScan)

    # force plugins to process
    scan.interpret()

    assert os.path.exists(testpath)
    nexus_output_file_name = (
        os.path.join(testpath, os.path.basename(os.path.splitext(TEST_SPEC_FILE)[0]),)
        + ".h5"
    )
    assert not os.path.exists(nexus_output_file_name)

    out = writer.Writer(sdf)
    out.save(nexus_output_file_name, [scanNum, ])

    assert os.path.exists(nexus_output_file_name)
    with h5py.File(nexus_output_file_name, "r") as h5:
        # check the NXentry/positioners:NXnote group
        assert "/S1/positioners" in h5

        pg = h5["/S1/positioners"]
        assert isinstance(pg, h5py.Group)
        assert hasattr(pg, "attrs")
        assert pg.attrs.get("NX_class") == "NXnote"
        assert pg.attrs.get("target") != pg.name

        for var in "Chi DCM_theta Delta GammaScrew Motor_10".split():
            assert var in pg
            child = pg[var]
            assert isinstance(child, h5py.Group)
            assert hasattr(child, "attrs")
            assert "NX_class" in child.attrs
            assert child.attrs["NX_class"] == "NXpositioner"
            assert "name" in child
            assert child["name"][()] == var.encode()
            assert "value" in child
            assert child["value"][()].shape == (1,)

        # check the NXentry/NXinstrument/positioners link
        assert "/S1/instrument/positioners" in h5

        ipg = h5["/S1/instrument/positioners"]
        assert isinstance(ipg, h5py.Group)
        assert hasattr(ipg, "attrs")
        assert pg.attrs.get("NX_class") == "NXnote"
        assert ipg.attrs.get("target") == ipg.name
        assert ipg.attrs.get("target") != pg.name


# -----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014-2022, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
