"""Tests for the writer module."""

import h5py
import os
import pytest

from . import _core
from ._core import hfile
from .. import spec
from .. import writer


def testWriter(hfile):
    """Test the writer.Writer class."""
    spec_file = os.path.join(_core.EXAMPLES_PATH, "33id_spec.dat")
    assert os.path.exists(spec_file)

    spec_data = spec.SpecDataFile(spec_file)
    out = writer.Writer(spec_data)
    scan_list = [1, 5, 7]
    out.save(hfile, scan_list)

    dd = out.root_attributes()
    assert isinstance(dd, dict)

    # TODO: test writer's various functions and methods

    # test file written by Writer
    with h5py.File(hfile, "r") as hp:
        root = hp["/"]
        default = root.attrs.get("default")
        assert default is not None
        assert default in root
        nxentry = root[default]

        default = nxentry.attrs.get("default")
        assert default is not None
        assert default in nxentry
        nxdata = nxentry[default]

        signal = nxdata.attrs.get("signal")
        assert signal is not None
        assert signal in nxdata


def test_save_data_mesh(hfile):
    # S 22  mesh  eta 57 57.1 10  chi 90.9 91 10  1
    spec_file = os.path.join(_core.EXAMPLES_PATH, "33id_spec.dat")
    assert os.path.exists(spec_file)

    spec_data = spec.SpecDataFile(spec_file)
    out = writer.Writer(spec_data)
    out.save(hfile, [22])

    with h5py.File(hfile, "r") as hp:
        root = hp["/"]
        nxdata = root["/S22/data"]
        signal = nxdata.attrs["signal"]
        assert nxdata[signal][()].shape == (11, 11)

        ds = nxdata["_mca_"]
        assert ds[()].shape == (11, 11, 91)
        assert ds.attrs["axes"] == "eta:chi:_mca_channel_"
        assert ds.attrs["spec_name"] == "_mca_"
        assert ds.attrs["units"] == "counts"


def test_save_data_hklmesh(hfile):
    # S 17  hklmesh  H 1.9 2.1 100  K 1.9 2.1 100  -800000
    spec_file = os.path.join(_core.EXAMPLES_PATH, "33bm_spec.dat")
    assert os.path.exists(spec_file)

    spec_data = spec.SpecDataFile(spec_file)
    out = writer.Writer(spec_data)
    out.save(hfile, [17])

    with h5py.File(hfile, "r") as hp:
        root = hp["/"]
        nxdata = root["/S17/data"]
        signal = nxdata.attrs["signal"]
        axes = nxdata.attrs["axes"]
        assert bytes(axes[0].encode("utf8")) == b"H"
        assert bytes(axes[1].encode("utf8")) == b"K"
        assert signal == "signal"


@pytest.mark.parametrize(
    "filename, scan_number, signal, axes",
    [
        ["lmn40.spe", 74, "NaI", "H"],
        ["33id_spec.dat", 104, "I0", "K"],
        ["33bm_spec.dat", 14, "signal", "L"],
    ],
)
def test_hkl_scans(filename, scan_number, signal, axes, hfile):
    spec_file = os.path.join(_core.EXAMPLES_PATH, filename)
    assert os.path.exists(spec_file)

    spec_data = spec.SpecDataFile(spec_file)
    out = writer.Writer(spec_data)
    out.save(hfile, [scan_number])

    with h5py.File(hfile, "r") as hp:
        root = hp["/"]
        nxdata = root["/S%d/data" % scan_number]
        assert nxdata.attrs["signal"] == signal
        assert nxdata.attrs["axes"] == axes


# -----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014-2022, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
