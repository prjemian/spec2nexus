#!/usr/bin/env python 
# -*- coding: utf-8 -*-

'''prjPySpec plugins for control lines defined by APS UNICAT'''

#-----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
#-----------------------------------------------------------------------------


from spec2nexus.plugin import ControlLineHandler


class MetadataMnes(ControlLineHandler):
    key_regexp = '#H\d+'


class MetadataValues(ControlLineHandler):
    key_regexp = '#V\d+'
