#!/usr/bin/env python 
# -*- coding: utf-8 -*-

'''
define custom control lines for SPEC data files

use this to test the plugin architecture
'''

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


class Pete(ControlLineHandler):
    key_regexp = '#Pete'


class Alta(ControlLineHandler):
    key_regexp = '#Alta'
