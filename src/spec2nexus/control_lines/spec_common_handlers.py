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


import re
from spec2nexus.plugin import ControlLineHandler
from spec2nexus.pySpec import SpecDataFileHeader, SpecDataFileScan, DuplicateSpecScanNumber, strip_first_word

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# header block

# TODO: add comment to each class

class CL_File(ControlLineHandler):
    key_regexp = '#F'
    
    def process(self, text, spec_file_obj, *args, **kws):
        spec_file_obj.specFile = strip_first_word(text)


class CL_Epoch(ControlLineHandler):
    key_regexp = '#E'
    
    def process(self, buf, spec_obj, *args, **kws):
        header = SpecDataFileHeader(buf, parent=spec_obj)
        line = buf.splitlines()[0].strip()
        header.epoch = int(strip_first_word(line))
        header.interpret()                  # parse the full header
        spec_obj.headers.append(header)
        


class CL_Date(ControlLineHandler):
    key_regexp = '#D'
    
    def process(self, text, spec_obj, *args, **kws):
        spec_obj.date = strip_first_word(text)


class CL_Comment(ControlLineHandler):
    key_regexp = '#C'
    
    def process(self, text, spec_obj, *args, **kws):
        spec_obj.comments.append( strip_first_word(text) )

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# scan block

class CL_Geometry(ControlLineHandler):
    key_regexp = '#G\d+'
    
    def process(self, text, spec_obj, *args, **kws):
        subkey = text.split()[0].lstrip('#')
        spec_obj.G[subkey] = strip_first_word(text)

class CL_NormalizingFactor(ControlLineHandler):
    key_regexp = 'I'

class CL_CounterNames(ControlLineHandler):
    key_regexp = '#J\d+'
    
    def process(self, text, spec_obj, *args, **kws):
        pass

class CL_CounterMnes(ControlLineHandler):
    key_regexp = '#j\d+'
    
    def process(self, text, spec_obj, *args, **kws):
        pass

class CL_Labels(ControlLineHandler):
    key_regexp = '#L'
    
    def process(self, text, spec_obj, *args, **kws):
        # Some folks use more than two spaces!  Use regular expression(re) module
        spec_obj.L = re.split("  +", strip_first_word(text))
        spec_obj.column_first = spec_obj.L[0]
        spec_obj.column_last = spec_obj.L[-1]

class CL_Monitor(ControlLineHandler):
    key_regexp = '#M'
    
    def process(self, text, spec_obj, *args, **kws):
        spec_obj.M, dname = strip_first_word(text).split()
        spec_obj.monitor_name = dname.lstrip('(').rstrip(')')

class CL_NumColumns(ControlLineHandler):
    key_regexp = '#N'
    
    def process(self, text, spec_obj, *args, **kws):
        spec_obj.N = int(strip_first_word(text))

class CL_PositionerNames(ControlLineHandler):
    key_regexp = '#O\d+'
    
    def process(self, text, spec_obj, *args, **kws):
        spec_obj.O.append( strip_first_word(text).split() )

class CL_PositionerMnes(ControlLineHandler):
    key_regexp = '#o\d+'
    
    def process(self, text, spec_obj, *args, **kws):
        pass

class CL_Positioners(ControlLineHandler):
    key_regexp = '#P\d+'
    
    def process(self, text, spec_obj, *args, **kws):
        spec_obj.P.append( strip_first_word(text) )     # TODO: what about post-processing?

class CL_HKL(ControlLineHandler):
    key_regexp = '#Q'
    
    def process(self, text, spec_obj, *args, **kws):
        spec_obj.Q = strip_first_word(text)

class CL_Scan(ControlLineHandler):
    key_regexp = '#S'
    
    def process(self, part, spec_obj, *args, **kws):
        scan = SpecDataFileScan(spec_obj.headers[-1], part, parent=spec_obj)
        text = part.splitlines()[0].strip()
        scan.S = strip_first_word(text)
        pos = scan.S.find(' ')
        scan.scanNum = int(scan.S[0:pos])
        scan.scanCmd = strip_first_word(scan.S[pos+1:])
        if scan.scanNum in spec_obj.scans:
            msg = str(scan.scanNum) + ' in ' + spec_obj.fileName
            raise DuplicateSpecScanNumber(msg)
        spec_obj.scans[scan.scanNum] = scan

class CL_Time(ControlLineHandler):
    key_regexp = '#T'
    
    def process(self, text, spec_obj, *args, **kws):
        spec_obj.T = strip_first_word(text).split()[0]

class CL_Temperature(ControlLineHandler):
    key_regexp = '#X'

class CL_DataLine(ControlLineHandler):
    key_regexp = '\d+'      # TODO: need more general regexp for signed data
    
    def process(self, text, spec_obj, *args, **kws):
        spec_obj.data_lines.append(text)

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
