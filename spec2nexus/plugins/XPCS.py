#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -----------------------------------------------------------------------------
# :author:    John Hammonds
# :email:     JPHammonds@anl.gov
# -----------------------------------------------------------------------------

"""
SPEC data file control lines unique to the APS XPCS instrument
"""

from spec2nexus.eznx import makeGroup
from spec2nexus.plugin_core import ControlLineBase
from spec2nexus.spec import SpecDataFileHeader, SpecDataFileScan
from spec2nexus.utils import strip_first_word


class XPCS_VA(ControlLineBase):
    """**#VA**"""

    key = r"#VA\d+"
    scan_attributes_defined = ["VA"]

    def process(self, text, spec_obj, *args, **kws):
        subkey = text.split()[0].lstrip("#")
        if not hasattr(spec_obj, "VA"):
            spec_obj.VA = {}
        spec_obj.VA[subkey] = strip_first_word(text)
        if isinstance(spec_obj, SpecDataFileHeader):
            spec_obj.addH5writer(self.key, self.writer)

    def writer(self, h5parent, writer, scan, nxclass=None, *args, **kws):
        """ Describe how to write VA data"""
        desc = "XPCS VA parameters"
        group = makeGroup(h5parent, "VA", nxclass, description=desc)
        dd = {}
        for item, value in scan.VA.items():
            dd[item] = list(map(str, value.split()))
        writer.save_dict(group, dd)


class XPCS_VD(ControlLineBase):
    """**#VD** """

    key = r"#VD\d+"
    scan_attributes_defined = ["VD"]

    def process(self, text, spec_obj, *args, **kws):
        subkey = text.split()[0].lstrip("#")
        if not hasattr(spec_obj, "VD"):
            spec_obj.VD = {}

        spec_obj.VD[subkey] = strip_first_word(text)
        if isinstance(spec_obj, SpecDataFileHeader):
            spec_obj.addH5writer(self.key, self.writer)

    def writer(self, h5parent, writer, scan, nxclass=None, *args, **kws):
        """Describe how to write VD data"""
        desc = "XPCS VD parameters"
        group = makeGroup(h5parent, "VD", nxclass, description=desc)
        dd = {}
        for item, value in scan.VD.items():
            dd[item] = list(map(str, value.split()))
        writer.save_dict(group, dd)


class XPCS_VE(ControlLineBase):
    """**#VE** """

    key = r"#VE\d+"
    scan_attributes_defined = ["VE"]

    def process(self, text, spec_obj, *args, **kws):
        subkey = text.split()[0].lstrip("#")
        if not hasattr(spec_obj, "VE"):
            spec_obj.VE = {}

        spec_obj.VE[subkey] = strip_first_word(text)
        if isinstance(spec_obj, SpecDataFileHeader):
            spec_obj.addH5writer(self.key, self.writer)

    def writer(self, h5parent, writer, scan, nxclass=None, *args, **kws):
        """Describe how to write VE data"""
        desc = "XPCS VE parameters"
        group = makeGroup(h5parent, "VE", nxclass, description=desc)
        dd = {}
        for item, value in scan.VE.items():
            dd[item] = list(map(str, value.split()))
        writer.save_dict(group, dd)


class XPCS_XPCS(ControlLineBase):
    """#XPCS"""

    key = r"#XPCS"
    scan_attributes_defined = ["XPCS"]

    def process(self, text, spec_obj, *args, **kws):
        if not hasattr(spec_obj, "XPCS"):
            spec_obj.XPCS = {}
        splitWord = strip_first_word(text).split()
        spec_obj.XPCS[splitWord[0]] = splitWord[1:]
        if isinstance(spec_obj, SpecDataFileScan):
            spec_obj.addH5writer(self.key, self.writer)

    def writer(self, h5parent, writer, scan, nxclass=None, *args, **kws):
        pass


class XPCS_CCD(ControlLineBase):
    """#CCD"""

    key = r"#CCD"
    scan_attributes_defined = ["CCD"]

    def process(self, text, spec_obj, *args, **kws):
        if not hasattr(spec_obj, "CCD"):
            spec_obj.CCD = {}
        splitWord = strip_first_word(text).split()
        spec_obj.CCD[splitWord[0]] = splitWord[1:]
        if isinstance(spec_obj, SpecDataFileScan):
            spec_obj.addH5writer(self.key, self.writer)

    def writer(self, h5parent, writer, scan, nxclass=None, *args, **kws):
        pass
