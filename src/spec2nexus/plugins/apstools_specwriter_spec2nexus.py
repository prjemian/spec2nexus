#!/usr/bin/env python 
# -*- coding: utf-8 -*-

#-----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014-2017, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
#-----------------------------------------------------------------------------

"""
**#MD** : Bluesky metadata from apstools SpecWriterCallback
"""

"""
#MD APSTOOLS_VERSION = 1.1.0
#MD BLUESKY_VERSION = 1.5.2
#MD EPICS_CA_MAX_ARRAY_BYTES = 1280000
#MD EPICS_HOST_ARCH = linux-x86_64
#MD OPHYD_VERSION = 1.3.2
#MD beamline_id = APS USAXS 9-ID-C
#MD datetime = 2019-04-19 10:04:44.400750
#MD login_id = usaxs@usaxscontrol.xray.aps.anl.gov
#MD pid = 27062
#MD proposal_id = testing Bluesky installation
#MD purpose = tuner
#MD tune_md = {'width': -0.004, 'initial_position': 8.824885, 'time_iso8601': '2019-04-19 10:04:44.402643'}
#MD tune_parameters = {'num': 31, 'width': -0.004, 'initial_position': 8.824885, 'peak_choice': 'com', 'x_axis': 'm_stage_r', 'y_axis': 'I0_USAXS'}
"""

from spec2nexus.plugin import ControlLineHandler
from collections import OrderedDict

class MD_apstools(ControlLineHandler):

    """**#MD** -- Bluesky metadata from apstools SpecWriterCallback"""

    key = '#MD\w*'
    
    def process(self, text, spec_obj, *args, **kws):
        if not hasattr(spec_obj, 'MD'):
            spec_obj.MD = OrderedDict()

        key = text.split()[1]
        p = text.find("=")
        value = text[p+1:].strip()
        # TODO: try to interpret as other than text?  ... Not yet.
        spec_obj.MD[key] = value
