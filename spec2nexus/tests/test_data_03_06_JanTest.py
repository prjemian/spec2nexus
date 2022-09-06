"""Unit tests for a specific data file."""

import h5py
import os

from ._core import EXAMPLES_PATH
from ._core import hfile
from .. import spec
from .. import writer


def test_the_data_file(hfile):
    """
    Write all as HDF5.

    * 1-D scans
    * USAXS scans
    * Fly scans
    * #O+#o and #J+#j control lines
    """
    file1 = os.path.join(EXAMPLES_PATH, "03_06_JanTest.dat")

    specfile = spec.SpecDataFile(file1)
    assert isinstance(specfile, spec.SpecDataFile), file1

    specwriter = writer.Writer(specfile)
    assert isinstance(specwriter, writer.Writer), file1

    specwriter.save(hfile, sorted(specfile.getScanNumbers()))
    assert os.path.exists(hfile)

    def subgroup_list(h5parent, nxclass):
        children = []
        for item in sorted(h5parent):
            obj = h5parent[item]
            if isinstance(obj, h5py.Group):
                if obj.attrs.get("NX_class", "") == nxclass:
                    children.append(obj)
        return children

    with h5py.File(hfile, "r") as h5root:
        assert isinstance(h5root, h5py.File), hfile
        nxentry_groups = subgroup_list(h5root, "NXentry")
        assert len(nxentry_groups) > 0
        for nxentry in nxentry_groups:
            nxdata_groups = subgroup_list(nxentry, "NXdata")
            assert len(nxdata_groups) > 0
            for nxdata in nxdata_groups:
                signal = nxdata.attrs.get("signal")
                assert signal in nxdata

        default = h5root.attrs.get("default")
        assert default in h5root
        nxentry = h5root[default]

        default = nxentry.attrs.get("default")
        assert default in nxentry
        nxdata = nxentry[default]

        signal = nxdata.attrs.get("signal")
        assert signal in nxdata


# -----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014-2022, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
