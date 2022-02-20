"""Tests for the writer module."""

import h5py
import os
import pytest
import shutil
import sys
import tempfile

from . import _core
from ._core import testpath
from .. import nexus


ARGV0 = sys.argv[0]


@pytest.mark.parametrize(
    "filename, opts, noise",
    [
        ["02_03_setup.dat", "-f --%s   -s 46", "verbose"],
        ["33id_spec.dat", "-f --%s   -s 1,3-5,8", "verbose"],
        ["spec_from_spock.spc", "-f --%s   -s 116", "verbose"],
        ["mca_spectra_example.dat", "-f --%s   -s 1", "verbose"],
        ["xpcs_plugin_sample.spec", "-f --%s   -s 1", "verbose"],
        ["02_03_setup.dat", "-f --%s   -s 46", "quiet"],
        ["33id_spec.dat", "-f --%s   -s 1,3-5,8", "quiet"],
        ["spec_from_spock.spc", "-f --%s   -s 116", "quiet"],
        ["mca_spectra_example.dat", "-f --%s   -s 1", "quiet"],
        ["xpcs_plugin_sample.spec", "-f --%s   -s 1", "quiet"],
    ],
)
def test_example(filename, opts, noise, testpath):
    specfile = os.path.join(_core.EXAMPLES_PATH, filename)
    assert os.path.exists(specfile)
    assert os.path.exists(testpath)

    shutil.copy2(specfile, testpath)
    # cmd = filename + "  " + opts
    sys.argv = [ARGV0, filename] + (opts % noise).split()

    nexus.main()

    hn = os.path.splitext(filename)[0] + ".hdf5"
    assert os.path.exists(hn)
    with h5py.File(hn, "r") as nx:
        assert isinstance(nx, h5py.File), "is HDF5 file"

        root = nx.get("/")
        assert root is not None, "HDF5 file has root element"
        comments = root.attrs.get("SPEC_comments")
        assert comments is not None, "HDF5 file has SPEC comments"
        default = root.attrs.get("default")
        assert default is not None, "HDF5 file has default attribute"

        nxentry = root[default]
        assert nxentry is not None, "HDF5 file has NXentry group"
        assert isinstance(nxentry, h5py.Group), default + " is HDF5 Group"

        default = nxentry.attrs.get("default")
        assert default is not None, default + " group has default attribute"
        nxdata = nxentry[default]
        assert nxdata is not None, "NXentry group has NXdata group"
        assert isinstance(nxdata, h5py.Group), default + " is HDF5 Group"


# -----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014-2022, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
