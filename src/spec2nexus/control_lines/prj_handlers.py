#!/usr/bin/env python 
# -*- coding: utf-8 -*-

'''
provide SPEC data file header
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
    plugin_name = '#Pete'


class Alta(ControlLineHandler):
    plugin_name = '#Alta'
