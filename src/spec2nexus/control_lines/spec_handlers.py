#!/usr/bin/env python 
# -*- coding: utf-8 -*-

'''
provide SPEC data file header

Also serves as an example of a Control Line plugin file.
Can define handlers for one or more Control Lines.
Each handler is a subclass of spec2nexus.plugin.ControlLineHandler
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


class F_line(ControlLineHandler):
    plugin_name = '#F'


class E_line(ControlLineHandler):
    plugin_name = '#E'


class D_line(ControlLineHandler):
    plugin_name = '#D'
