#!/usr/bin/env python 
# -*- coding: utf-8 -*-

'''
SPEC standard data file support

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
from spec2nexus.spec import SpecDataFileHeader, SpecDataFileScan, DuplicateSpecScanNumber
from spec2nexus.utils import strip_first_word
from spec2nexus import eznx

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# header block

class SPEC_File(ControlLineHandler):
    '''**#F** -- original data file name (starts a file header block)'''

    key = '#F'
    
    def process(self, text, spec_file_obj, *args, **kws):
        spec_file_obj.specFile = strip_first_word(text)


class SPEC_Epoch(ControlLineHandler):
    '''
    **#E** -- the UNIX epoch (seconds from 00:00 GMT 1/1/70)
    
    In SPEC data files, the ``#E`` control line indicates the 
    start of a *header* block.
    '''

    key = '#E'
    
    def process(self, buf, scan, *args, **kws):
        header = SpecDataFileHeader(buf, parent=scan)
        line = buf.splitlines()[0].strip()
        header.epoch = int(strip_first_word(line))
        header.interpret()                  # parse the full header
        scan.headers.append(header)
        


class SPEC_Date(ControlLineHandler):
    '''**#D** -- date/time stamp'''

    key = '#D'
    
    def process(self, text, scan, *args, **kws):
        scan.date = strip_first_word(text)


class SPEC_Comment(ControlLineHandler):
    '''**#C** -- any comment either in the scan header or somewhere in the scan'''

    key = '#C'
    
    def process(self, text, scan, *args, **kws):
        scan.comments.append( strip_first_word(text) )

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# scan block

class SPEC_Geometry(ControlLineHandler):
    '''
    **#G** -- diffractometer geometry (numbered rows: #G0, #G1, ...)
    '''

    key = '#G\d+'
    
    def process(self, text, scan, *args, **kws):
        subkey = text.split()[0].lstrip('#')
        scan.G[subkey] = strip_first_word(text)
        if len(scan.G) > 0:
            scan.addH5writer('G_writer', self.writer)
    
    def writer(self, h5parent, writer, default_nxclass, scan, *args, **kws):
        '''Describe how to store this data in an HDF5 NeXus file'''
        # e.g.: SPECD/four.mac
        # http://certif.com/spec_manual/fourc_4_9.html
        desc = "SPEC geometry arrays, meanings defined by SPEC diffractometer support"
        group = eznx.makeGroup(h5parent, 'G', default_nxclass, description=desc)
        dd = {}
        for item, value in scan.G.items():
            dd[item] = map(float, value.split())
        writer.save_dict(group, dd)


class SPEC_NormalizingFactor(ControlLineHandler):
    '''**#I** -- intensity normalizing factor'''

    key = '#I'

    def process(self, text, scan, *args, **kws):
        scan.I = float(strip_first_word(text))

class SPEC_CounterNames(ControlLineHandler):
    '''**#J** -- names of counters (each separated by two spaces) (ignored for now)'''

    key = '#J\d+'
    
    def process(self, text, scan, *args, **kws):
        pass    # ignore this for now

class SPEC_CounterMnemonics(ControlLineHandler):
    '''**#j** -- mnemonics of counter (% = 0,1,2,... with eight counters per row) (ignored for now)'''

    key = '#j\d+'
    
    def process(self, text, scan, *args, **kws):
        pass    # ignore this for now

class SPEC_Labels(ControlLineHandler):
    '''**#L** -- data column labels'''

    key = '#L'
    
    def process(self, text, scan, *args, **kws):
        # Some folks use more than two spaces!  Use regular expression(re) module
        scan.L = re.split("  +", strip_first_word(text))
        scan.column_first = scan.L[0]
        scan.column_last = scan.L[-1]

class SPEC_Monitor(ControlLineHandler):
    '''
    **#M** -- counting against this constant monitor count (see #T)
    '''

    key = '#M'
    
    def process(self, text, scan, *args, **kws):
        scan.M, dname = strip_first_word(text).split()
        scan.monitor_name = dname.lstrip('(').rstrip(')')

class SPEC_NumColumns(ControlLineHandler):
    '''
    **#N** -- number of columns of data [ num2 sets per row ]
    '''

    key = '#N'
    # TODO: Needs an example data file to test (issue #8)
    
    def process(self, text, scan, *args, **kws):
        scan.N = map(int, strip_first_word(text).split())

class SPEC_PositionerNames(ControlLineHandler):
    '''**#O** -- positioner names (numbered rows: #O0, #O1, ...)'''

    key = '#O\d+'
    
    def process(self, text, scan, *args, **kws):
        scan.O.append( strip_first_word(text).split() )

class SPEC_PositionerMnemonics(ControlLineHandler):
    '''**#o** -- positioner mnemonics (ignored for now)'''

    key = '#o\d+'
    
    def process(self, text, scan, *args, **kws):
        pass    # ignore this for now


class SPEC_Positioners(ControlLineHandler):
    '''**#P** -- positioner values at start of scan (numbered rows: #P0, #P1, ...)'''

    key = '#P\d+'
    
    def process(self, text, scan, *args, **kws):
        scan.P.append( strip_first_word(text) )
        scan.addPostProcessor('motor_positions', self.postprocess)
    
    def postprocess(self, scan, *args, **kws):
        '''
        interpret the motor positions from the scan header
        
        :param SpecDataFileScan scan: data from a single SPEC scan
        '''
        scan.positioner = {}
        for row, values in enumerate(scan.P):
            for col, val in enumerate(values.split()):
                if row >= len(scan.header.O):
                    pass
                if col >= len(scan.header.O[row]):
                    pass
                mne = scan.header.O[row][col]
                scan.positioner[mne] = float(val)
        if len(scan.positioner) > 0:
            scan.addH5writer(self.key, self.writer)
    
    def writer(self, h5parent, writer, nxclass, scan, *args, **kws):
        '''Describe how to store this data in an HDF5 NeXus file'''
        desc='SPEC positioners (#P & #O lines)'
        group = eznx.makeGroup(h5parent, 'positioners', nxclass, description=desc)
        writer.save_dict(group, scan.positioner)


class SPEC_HKL(ControlLineHandler):
    '''**#Q** -- :math:`Q` (:math:`hkl`) at start of scan'''

    key = '#Q'
    
    def process(self, text, scan, *args, **kws):
        s = strip_first_word(text)
        if len(s) > 0:
            scan.Q = map(float, s.split())
            scan.addH5writer('Q_writer', self.writer)
    
    def writer(self, h5parent, writer, default_nxclass, scan, *args, **kws):
        '''Describe how to store this data in an HDF5 NeXus file'''
        desc = 'hkl at start of scan'
        eznx.write_dataset(h5parent, "Q", scan.Q, description = desc)


class SPEC_Scan(ControlLineHandler):
    '''
    **#S** -- SPEC scan
    
    In SPEC data files, the ``#S`` control line indicates the 
    start of a *scan* block.
    '''

    key = '#S'
    
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

class SPEC_CountTime(ControlLineHandler):
    '''
    **#T** -- counting against this constant number of seconds (see #M)
    '''

    key = '#T'
    
    def process(self, text, scan, *args, **kws):
        scan.T = strip_first_word(text).split()[0]

class SPEC_TemperatureSetPoint(ControlLineHandler):
    '''**#X** -- Temperature'''

    key = '#X'
    # TODO: Needs an example data file to test
    
    def process(self, text, scan, *args, **kws):
        try:
            x = float( strip_first_word(text) )
        except ValueError:
            # FIXME: resolve how to store this
            # #X       setpoint       The temperature setpoint. 
            # def Fheader '_cols++;printf("#X %gKohm (%gC)\n",TEMP_SP,DEGC_SP)'
            x = strip_first_word(text)  # might have trailing text: 12.345kZ
        scan.X = x

class SPEC_DataLine(ControlLineHandler):
    '''**(scan data)** -- scan data line'''

    # key = r'[+-]?\d*\.?\d?'
    # use custom key match since regexp for floats is tedious!
    key = r'scan data'
    def match_key(self, text):
        '''
        Easier to try conversion to number than construct complicated regexp
        '''
        try:
            float( text.strip().split()[0] )
            return True
        except ValueError:
            return False
    
    def process(self, text, scan, *args, **kws):
        scan.data_lines.append(text)
        
        # defer processing since comments and MCA data may intersperse the scan data
        scan.addPostProcessor('scan data', self.postprocess)
    
    def postprocess(self, scan, *args, **kws):
        data_lines_postprocessing(scan)
    

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# MCA: multi-channel analyzer

# see ESRF BLISS group: http://www.esrf.eu/blissdb/macros/getsource.py?macname=mca.mac

class SPEC_MCA(ControlLineHandler):
    '''
    **#@MCA** -- declares this scan contains MCA data (array_dump() format, as in ``"%16C"``)
    '''

    key = '#@MCA'

    '''
    #@MCA 16C 
    Format string passed to data_dump() function. 
    This format string is held by the global variable "MCA_FMT" and can then been adapted to particular needs. 
    "%%16C" is the default. It dumps data on 1 line, cut every 16 points::
    
        @A 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\
         0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\
         0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\
         0 0 0 0 0 0 0 0 0 0 0 ...
    
    "%%16" would do the same without any backslash
    "1" would dump 1 point per line, ...
    '''
    
    def process(self, text, scan, *args, **kws):
        # #@MCA 16C
        # Isn't this only informative to how the data is presented in the file?
        pass        # not sure how to handle this, ignore it for now

class SPEC_MCA_Array(ControlLineHandler):
    '''
    **@A** -- MCA Array data
    
    MCA data. Each value is the content of one channel, or an 
    integrated value over several channels if a reduction was applied.
    '''

    key = '@A'
    # continued lines will be matched by SPEC_DataLine
    # process these lines only after all lines have been read

    # TODO: need more examples of MCA spectra in SPEC files to improve this
    # Are there any other MCA spectra (such as @B) possible?
    
    def process(self, text, scan, *args, **kws):
        # acquire like numerical data, handle in postprocessing
        scan.data_lines.append(text)
        scan.addPostProcessor('scan data', self.postprocess)
    
    def postprocess(self, scan, *args, **kws):
        data_lines_postprocessing(scan)

class SPEC_MCA_Calibration(ControlLineHandler):
    '''**#@CALIB** -- coefficients for :math:`x_k = a +bk + ck^2` for MCA data, k is channel number'''

    key = '#@CALIB'
    
    def process(self, text, scan, *args, **kws):
        # #@CALIB a b c
        s = strip_first_word(text).split()
        a, b, c = map(float, s)
        
        if not hasattr(scan, 'MCA'):
            scan.MCA = {}
        if 'CALIB' not in scan.MCA:
            scan.MCA['CALIB'] = {}

        scan.MCA['CALIB']['a'] = a
        scan.MCA['CALIB']['b'] = b
        scan.MCA['CALIB']['c'] = c

class SPEC_MCA_ChannelInformation(ControlLineHandler):
    '''**#@CHANN** -- MCA channel information (number_saved, first_saved, last_saved, reduction_coef)'''

    key = '#@CHANN'
    
    def process(self, text, scan, *args, **kws):
        # #@CHANN 1201 1110 1200 1
        s = strip_first_word(text).split()
        number_saved, first_saved, last_saved = map(int, s[0:3])
        reduction_coef = float(s[-1])

        if not hasattr(scan, 'MCA'):
            scan.MCA = {}

        scan.MCA['number_saved'] = number_saved
        scan.MCA['first_saved'] = first_saved
        scan.MCA['last_saved'] = last_saved
        scan.MCA['reduction_coef'] = reduction_coef


class SPEC_MCA_CountTime(ControlLineHandler):
    '''**#@CTIME** -- MCA count times (preset_time, elapsed_live_time, elapsed_real_time)'''

    key = '#@CTIME'
    
    def process(self, text, scan, *args, **kws):
        s = strip_first_word(text).split()
        preset_time, elapsed_live_time, elapsed_real_time = map(float, s)

        if not hasattr(scan, 'MCA'):
            scan.MCA = {}

        scan.MCA['preset_time'] = preset_time
        scan.MCA['elapsed_live_time'] = elapsed_live_time
        scan.MCA['elapsed_real_time'] = elapsed_real_time


class SPEC_MCA_RegionOfInterest(ControlLineHandler):
    '''**#@ROI** -- MCA ROI channel information (ROI_name, first_chan, last_chan)'''

    key = '#@ROI'
    
    def process(self, text, scan, *args, **kws):
        s = strip_first_word(text).split()
        ROI_name = s[0]
        first_chan, last_chan = map(int, s[1:])

        if not hasattr(scan, 'MCA'):
            scan.MCA = {}
        if 'ROI' not in scan.MCA:
            scan.MCA['ROI'] = {}

        scan.MCA['ROI'][ROI_name] = {}
        scan.MCA['ROI'][ROI_name]['first_chan'] = first_chan
        scan.MCA['ROI'][ROI_name]['last_chan'] = last_chan

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def data_lines_postprocessing(scan):
    '''
    interpret the data lines from the body of the scan
    
    :param SpecDataFileScan scan: data from a single SPEC scan
    '''
    # first, get the column labels, rename redundant labels to be unique
    # the unique labels will be the scan.data dictionary keys
    scan.data = {}
    for col in range(len(scan.L)):
        label = scan._unique_key(scan.L[col], scan.data.keys())
        # need to guard when same column label is used more than once
        if label != scan.L[col]:
            scan.L[col] = label     # rename this column's label
        scan.data[label] = []       # list for the column's data
    num_columns = len(scan.data)
    
    # gather up any continuation lines
    dl = '\n'.join(scan.data_lines).replace('\\\n', ' ')
    if dl.find('@A') > -1:
        # Can there be more than 1 MCA spectrum specified?
        scan.data['_mca_'] = []

    # interpret the data lines from the body of the scan
    for _, values in enumerate(dl.splitlines()):
        if values.startswith('@A'):
            # accumulate this spectrum
            mca_spectrum = map(float, values[2:].split())
            scan.data['_mca_'].append(mca_spectrum)
        else:
            buf = scan._interpret_data_row(values)
            if len(buf) == num_columns:
                # only keep complete rows
                for label, val in buf.items():
                    scan.data[label].append(val)
