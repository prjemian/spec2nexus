#!/usr/bin/env python 
# -*- coding: utf-8 -*-

'''
provide SPEC data file header

Also serves as an example of a Control Line plugin file.
Can define handlers for one or more Control Lines.
Each handler is a subclass of spec2nexus.plugin.ControlLineHandler

:see: SPEC manual, *Standard Data File Format*, http://www.certif.com/spec_manual/user_1_4_1.html
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

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# header block

class CL_File(ControlLineHandler):
    key_regexp = '#F'


class CL_Epoch(ControlLineHandler):
    key_regexp = '#E'


class CL_Date(ControlLineHandler):
    key_regexp = '#D'


class CL_Comment(ControlLineHandler):
    key_regexp = '#C'

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# scan block

class CL_Geometry(ControlLineHandler):
    key_regexp = '#G\d+'

class CL_NormalizingFactor(ControlLineHandler):
    key_regexp = 'I'

class CL_Labels(ControlLineHandler):
    key_regexp = '#L'

class CL_Monitor(ControlLineHandler):
    key_regexp = '#M'

class CL_NumColumns(ControlLineHandler):
    key_regexp = '#N'

class CL_PositionerMnes(ControlLineHandler):
    key_regexp = '#O\d+'

class CL_Positioners(ControlLineHandler):
    key_regexp = '#P\d+'

class CL_HKL(ControlLineHandler):
    key_regexp = '#Q'

class CL_Scan(ControlLineHandler):
    key_regexp = '#S'

class CL_Time(ControlLineHandler):
    key_regexp = '#T'

class CL_Temperature(ControlLineHandler):
    key_regexp = 'X'

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# MCA: multi-channel analyzer

class CL_MCA(ControlLineHandler):
    key_regexp = '#@MCA'

class CL_MCA_Array(ControlLineHandler):
    key_regexp = '@A'

class CL_MCA_Calibration(ControlLineHandler):
    key_regexp = '#@CALIB'

class CL_MCA_ChannelInformation(ControlLineHandler):
    key_regexp = '#@CHANN'

class CL_MCA_CountTime(ControlLineHandler):
    key_regexp = '#@CTIME'

class CL_MCA_RegionOfInterest(ControlLineHandler):
    key_regexp = '#@ROI'
