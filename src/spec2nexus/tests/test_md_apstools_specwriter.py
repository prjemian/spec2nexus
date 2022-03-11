"""
unit tests for a specific data file, look for Bluesky metadata
"""

import h5py
import os

from .. import spec
from .. import writer

from ._core import EXAMPLES_PATH
from ._core import hfile

TESTFILE = os.path.join(EXAMPLES_PATH, "usaxs-bluesky-specwritercallback.dat")


def test_the_data_file(hfile):
    """
    look for the metadata
    """
    specfile = spec.SpecDataFile(TESTFILE)
    assert isinstance(specfile, spec.SpecDataFile), TESTFILE

    for scan_num, scan in specfile.scans.items():
        msg = "Scan %s MD test" % scan_num
        scan.interpret()  # force lazy-loader to parse this scan
        assert hasattr(scan, "MD"), msg
        assert isinstance(scan.MD, dict), msg
        assert len(scan.MD) > 0, msg

    # test the metadata in a NeXus file

    specwriter = writer.Writer(specfile)
    assert isinstance(specwriter, writer.Writer), TESTFILE

    specwriter.save(hfile, sorted(specfile.getScanNumbers()))
    assert os.path.exists(hfile)

    def subgroup_list(parent, nxclass):
        children = []
        for item in sorted(parent):
            obj = parent[item]
            if isinstance(obj, h5py.Group):
                if obj.attrs.get("NX_class", "") == nxclass:
                    children.append(obj)
        return children

    with h5py.File(hfile, "r") as fp:
        for nxentry in subgroup_list(fp, "NXentry"):
            # nxinstrument_groups = subgroup_list(nxentry, 'NXinstrument')
            # self.assertEqual(len(nxinstrument_groups), 1)
            # nxinstrument = nxinstrument_groups[0]

            nxcollection_groups = subgroup_list(nxentry, "NXcollection")
            assert len(nxcollection_groups) > 0
            md_group = nxentry.get("bluesky_metadata")
            assert md_group is not None, "bluesky_metadata in NeXus file"

    os.remove(hfile)
    assert not os.path.exists(hfile)


# -----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014-2022, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
