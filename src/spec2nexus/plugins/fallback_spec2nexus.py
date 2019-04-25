#!/usr/bin/env python 
# -*- coding: utf-8 -*-

#-----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014-2019, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
#-----------------------------------------------------------------------------

"""
Fallback handling for any SPEC data file control lines not recognized by other handlers
"""

from collections import OrderedDict
from spec2nexus.plugin import ControlLineHandler
from spec2nexus.eznx import makeGroup
from spec2nexus.spec import SpecDataFileHeader, UNRECOGNIZED_KEY, SpecDataFileScan

class UnrecognizedControlLine(ControlLineHandler):
    
    """unrecognized control line"""

    key = UNRECOGNIZED_KEY

    def process(self, text, spec_obj, *args, **kws):
        ' '
        if not hasattr(spec_obj, '_unrecognized'):
            spec_obj._unrecognized = []
        spec_obj._unrecognized.append(text)
        if isinstance(spec_obj, SpecDataFileHeader) or isinstance(spec_obj, SpecDataFileScan):
            spec_obj.addH5writer(self.key, self.writer)
    
    def writer(self, h5parent, writer, scan, nxclass=None, *args, **kws):
        """write the data in a NeXus group named ``unrecognized``"""
        desc = "SPEC data file control lines not otherwise recognized"
        nxclass = 'NXnote'
        group = makeGroup(h5parent, 'unrecognized', nxclass, description=desc)
        dd = OrderedDict()
        for i, value in enumerate(scan._unrecognized):
            dd['u' + str(i)] = value
        writer.save_dict(group, dd)
