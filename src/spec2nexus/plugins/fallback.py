"""
Fallback handling for any SPEC data file control lines not recognized by other handlers
"""

# use absolute imports (not relative)
from spec2nexus.eznx import makeGroup
from spec2nexus.plugin_core import ControlLineBase
from spec2nexus.spec import UNRECOGNIZED_KEY
from spec2nexus.spec import SpecDataFileHeader
from spec2nexus.spec import SpecDataFileScan


class UnrecognizedControlLine(ControlLineBase):

    """unrecognized control line"""

    key = UNRECOGNIZED_KEY
    scan_attributes_defined = ["_unrecognized"]

    def process(self, text, spec_obj, *args, **kws):
        " "
        if not hasattr(spec_obj, "_unrecognized"):
            spec_obj._unrecognized = []
        spec_obj._unrecognized.append(text)
        if isinstance(spec_obj, (SpecDataFileHeader, SpecDataFileScan)):
            spec_obj.addH5writer(self.key, self.writer)

    def writer(self, h5parent, writer, scan, nxclass=None, *args, **kws):
        """write the data in a NeXus group named ``unrecognized``"""
        desc = "SPEC data file control lines not otherwise recognized"
        nxclass = "NXnote"
        i = 0
        success = False
        while not success:
            i += 1
            nm = "unrecognized_" + str(i)
            if nm not in h5parent.keys():
                group = makeGroup(h5parent, nm, nxclass, description=desc)
                success = True
        dd = {f"u{i}": value for i, value in enumerate(scan._unrecognized)}
        writer.save_dict(group, dd)

# -----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014-2022, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
