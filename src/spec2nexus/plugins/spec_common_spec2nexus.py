#!/usr/bin/env python 
# -*- coding: utf-8 -*-

'''
SPEC data file standard control lines

:see: SPEC manual, *Standard Data File Format*,
   http://www.certif.com/spec_manual/user_1_4_1.html

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
from spec2nexus.eznx import write_dataset, makeGroup, openGroup
from spec2nexus.plugin import ControlLineHandler
from spec2nexus.spec import SpecDataFileHeader, SpecDataFileScan, DuplicateSpecScanNumber
from spec2nexus.utils import strip_first_word, iso8601
from spec2nexus.scanf import scanf

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# header block

class SPEC_File(ControlLineHandler):
    '''
    **#F** -- original data file name (starts a file header block)
    
    Module :mod:`spec2nexus.spec` is responsible for handling this control line.
    
    IN-MEMORY REPRESENTATION
    
    * (SpecDataFile): **fileName**
    * (SpecDataFileHeader) : **file**
    
    HDF5/NeXus REPRESENTATION
    
    * file root-level attribute: **SPEC_file**
    '''

    key = '#F'
    
    def process(self, text, spec_file_obj, *args, **kws):
        spec_file_obj.specFile = strip_first_word(text)


class SPEC_Epoch(ControlLineHandler):
    '''
    **#E** -- the UNIX epoch (seconds from 00:00 GMT 1/1/70)
    
    In SPEC data files, the ``#E`` control line indicates the 
    start of a *header* block.
        
    IN-MEMORY REPRESENTATION
    
    * (SpecDataFileHeader): **epoch** *int*
    
    HDF5/NeXus REPRESENTATION
    
    * file root-level attribute: **SPEC_epoch** *int*
    '''

    key = '#E'
    
    def process(self, buf, scan, *args, **kws):
        header = SpecDataFileHeader(buf, parent=scan)
        line = buf.splitlines()[0].strip()
        header.epoch = int(strip_first_word(line))
        header.interpret()                  # parse the full header
        scan.headers.append(header)


class SPEC_Date(ControlLineHandler):
    '''
    **#D** -- date/time stamp
        
    IN-MEMORY REPRESENTATION
    
    * (SpecDataFileHeader): **date** *str*, ISO8601 format
    
    HDF5/NeXus REPRESENTATION
    
    * file root-level attribute: **SPEC_date** *str* (value for 1st header block is used)
    '''

    key = '#D'
    
    def process(self, text, scan, *args, **kws):
        scan.date = strip_first_word(text)
        if isinstance(scan, SpecDataFileScan):
            scan.addH5writer(self.key, self.writer)
    
    def writer(self, h5parent, writer, scan, *args, **kws):
        '''Describe how to store this data in an HDF5 NeXus file'''
        write_dataset(h5parent, "date", iso8601(scan.date)  )


class SPEC_Comment(ControlLineHandler):
    '''
    **#C** -- any comment either in the scan header or somewhere in the scan
        
    IN-MEMORY REPRESENTATION
    
    * (SpecDataFileHeader): **comments**
    * (SpecDataFileScan):  **comments**
    
    HDF5/NeXus REPRESENTATION
    
    * file root-level attribute: **SPEC_comments** : 
      string array of all comments from first header block
    * dataset named **comments** under */NXentry* group, such as */S1/comments* : 
      string array of all comments from this scan block
    
    '''

    key = '#C'
    
    def process(self, text, scan, *args, **kws):
        scan.comments.append( strip_first_word(text) )
        if isinstance(scan, SpecDataFileScan):
            scan.addH5writer(self.key, self.writer)
    
    def writer(self, h5parent, writer, scan, *args, **kws):
        '''Describe how to store this data in an HDF5 NeXus file'''
        write_dataset(h5parent, "comments", '\n'.join(scan.comments))

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# scan block


class SPEC_Scan(ControlLineHandler):
    '''
    **#S** -- SPEC scan
    
    In SPEC data files, the ``#S`` control line indicates the 
    start of a *scan* block.  Each scan will be written to a 
    separate **NXentry** group in the HDF5 file.
    
    **NXentry**:
        "The top-level NeXus group which contains all the data 
        and associated information that comprise a single measurement."
        
        -- http://download.nexusformat.org/doc/html/classes/base_classes/NXentry.html
        
    IN-MEMORY REPRESENTATION
    
    * (SpecDataFile): 
    * (SpecDataFileHeader): 
    
    HDF5/NeXus REPRESENTATION
    
    * */NXentry* group named 'S%d` scan_number at root 
      level, such as */S1*

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


class SPEC_Geometry(ControlLineHandler):
    '''
    **#G** -- diffractometer geometry (numbered rows: #G0, #G1, ...)
        
    IN-MEMORY REPRESENTATION
    
    * (SpecDataFileScan): **G**
    
    HDF5/NeXus REPRESENTATION
    
    * *NXcollection* group named **G** in the *NXentry* group, such as */S1/G*
      
      * Datasets created from dictionary <scan>.G 
        (indexed by number from the scan block, such as ``G0``, ``G1``, ...).
        Meaning of contents for each index are defined by geometry-specific 
        SPEC diffractometer support.

    '''

    key = '#G\d+'
    
    def process(self, text, scan, *args, **kws):
        subkey = text.split()[0].lstrip('#')
        scan.G[subkey] = strip_first_word(text)
        if len(scan.G) > 0:
            scan.addH5writer(self.key, self.writer)
    
    def writer(self, h5parent, writer, scan, nxclass=None, *args, **kws):
        '''Describe how to store this data in an HDF5 NeXus file'''
        # e.g.: SPECD/four.mac
        # http://certif.com/spec_manual/fourc_4_9.html
        desc = "SPEC geometry arrays, meanings defined by SPEC diffractometer support"
        group = makeGroup(h5parent, 'G', nxclass, description=desc)
        dd = {}
        for item, value in scan.G.items():
            dd[item] = map(float, value.split())
        writer.save_dict(group, dd)


class SPEC_NormalizingFactor(ControlLineHandler):
    '''
    **#I** -- intensity normalizing factor
        
    IN-MEMORY REPRESENTATION
    
    * (SpecDataFileScan): **I**
    
    HDF5/NeXus REPRESENTATION
    
    * Dataset named **intensity_factor** in the *NXentry* group, such as */S1/intensity_factor*
    '''

    key = '#I'

    def process(self, text, scan, *args, **kws):
        scan.I = float(strip_first_word(text))
    
    def writer(self, h5parent, writer, scan, nxclass=None, *args, **kws):
        '''Describe how to store this data in an HDF5 NeXus file'''
        if hasattr('I', scan):
            writer.write_dataset(h5parent, "intensity_factor", scan.I)


class SPEC_CounterNames(ControlLineHandler):
    '''**#J** -- names of counters (each separated by two spaces) (ignored for now)'''

    key = '#J\d+'
    
    def process(self, text, scan, *args, **kws):
        pass    # ignore this for now


class SPEC_CounterMnemonics(ControlLineHandler):
    '''**#j** -- mnemonics of counter  (ignored for now)'''

    key = '#j\d+'
    
    def process(self, text, scan, *args, **kws):
        pass    # ignore this for now


class SPEC_Labels(ControlLineHandler):
    '''
    **#L** -- data column labels
    
    IN-MEMORY REPRESENTATION
    
    * (SpecDataFileScan): **L** : labels
    * (SpecDataFileScan): **data** : {labels: values}
    
    HDF5/NeXus REPRESENTATION
    
    * *NXdata* group named **data** in the *NXentry* group, such as */S1/data*
      
      * datasets with names supplied in **L**, array values collected in **data_lines**

    '''

    key = '#L'
    
    def process(self, text, scan, *args, **kws):
        # Some folks use more than two spaces!  Use regular expression(re) module
        scan.L = re.split("  +", strip_first_word(text))
        scan.column_first = scan.L[0]
        scan.column_last = scan.L[-1]


class SPEC_Monitor(ControlLineHandler):
    '''
    **#M** -- counting against this constant monitor count (see #T)
        
    IN-MEMORY REPRESENTATION
    
    * (SpecDataFileScan): **M**
    
    HDF5/NeXus REPRESENTATION
    
    * Dataset named **M** in the *NXentry* group, such as */S1/M*
    * Dataset named **counting_basis** in the *NXentry* group with 
      value *SPEC scan with constant monitor count*, such as */S1/counting_basis*

    '''

    key = '#M'
    
    def process(self, text, scan, *args, **kws):
        scan.M, dname = strip_first_word(text).split()
        scan.monitor_name = dname.lstrip('(').rstrip(')')
        scan.addH5writer(self.key, self.writer)
    
    def writer(self, h5parent, writer, scan, *args, **kws):
        '''Describe how to store this data in an HDF5 NeXus file'''
        desc = 'SPEC scan with constant monitor count'
        write_dataset(h5parent, "counting_basis", desc)
        write_dataset(h5parent, "M", float(scan.M), units='counts', description = desc)


class SPEC_NumColumns(ControlLineHandler):
    '''
    **#N** -- number of columns of data [ num2 sets per row ]
    
    IN-MEMORY REPRESENTATION
    
    * (SpecDataFileScan): **N** : [int]
    
    HDF5/NeXus REPRESENTATION
    
    * not written to file
    '''

    key = '#N'
    # TODO: Needs an example data file to test (issue #8)
    
    def process(self, text, scan, *args, **kws):
        scan.N = map(int, strip_first_word(text).split())


class SPEC_PositionerNames(ControlLineHandler):
    '''
    **#O** -- positioner names (numbered rows: #O0, #O1, ...)
    
    IN-MEMORY REPRESENTATION
    
    * (SpecDataFileHeader) : **O** : label
    * (SpecDataFileScan): **positioner** : {label: value}
    
    HDF5/NeXus REPRESENTATION
    
    * *NXcollection* group named **positioners** in the *NXentry* group, such as */S1/positioners*
      
      * datasets created from dictionary <scan>.positioner

    '''

    key = '#O\d+'
    
    def process(self, text, scan, *args, **kws):
        scan.O.append( strip_first_word(text).split() )


class SPEC_PositionerMnemonics(ControlLineHandler):
    '''**#o** -- positioner mnemonics (ignored for now)'''

    key = '#o\d+'
    
    def process(self, text, scan, *args, **kws):
        pass    # ignore this for now


class SPEC_Positioners(ControlLineHandler):
    '''
    **#P** -- positioner values at start of scan (numbered rows: #P0, #P1, ...)
    
    IN-MEMORY REPRESENTATION
    
    * (SpecDataFileHeader) : **O** : label
    * (SpecDataFileScan): **positioner** : {label: value}
    
    HDF5/NeXus REPRESENTATION
    
    * *NXcollection* group named **positioners** in the *NXentry* group, such as */S1/positioners*
      
      * datasets created from dictionary <scan>.positioner

    '''

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
    
    def writer(self, h5parent, writer, scan, nxclass=None, *args, **kws):
        '''Describe how to store this data in an HDF5 NeXus file'''
        desc='SPEC positioners (#P & #O lines)'
        group = makeGroup(h5parent, 'positioners', nxclass, description=desc)
        writer.save_dict(group, scan.positioner)


class SPEC_HKL(ControlLineHandler):
    '''
    **#Q** -- :math:`Q` (:math:`hkl`) at start of scan
        
    IN-MEMORY REPRESENTATION
    
    * (SpecDataFileScan): **Q**
    
    HDF5/NeXus REPRESENTATION
    
    * Dataset named **Q** in the *NXentry* group, such as */S1/M*
    '''

    key = '#Q'
    
    def process(self, text, scan, *args, **kws):
        s = strip_first_word(text)
        if len(s) > 0:
            scan.Q = map(float, s.split())
            scan.addH5writer(self.key, self.writer)
    
    def writer(self, h5parent, writer, scan, *args, **kws):
        '''Describe how to store this data in an HDF5 NeXus file'''
        desc = 'hkl at start of scan'
        write_dataset(h5parent, "Q", scan.Q, description = desc)


class SPEC_CountTime(ControlLineHandler):
    '''
    **#T** -- counting against this constant number of seconds (see #M)
        
    IN-MEMORY REPRESENTATION
    
    * (SpecDataFileScan): **T**
    
    HDF5/NeXus REPRESENTATION
    
    * Dataset named **T** in the *NXentry* group, such as */S1/T*
    * Dataset named **counting_basis** in the *NXentry* group with 
      value *SPEC scan with constant counting time*, such as */S1/counting_basis*

    '''

    key = '#T'
    
    def process(self, text, scan, *args, **kws):
        scan.T = strip_first_word(text).split()[0]
        scan.addH5writer(self.key, self.writer)
    
    def writer(self, h5parent, writer, scan, *args, **kws):
        '''Describe how to store this data in an HDF5 NeXus file'''
        desc = 'SPEC scan with constant counting time'
        write_dataset(h5parent, "counting_basis", desc)
        write_dataset(h5parent, "T", float(scan.T), units='s', description = desc)


class SPEC_TemperatureSetPoint(ControlLineHandler):
    '''
    **#X** -- Temperature
    
    The default declaration of the #X control line is written::
    
         def Fheader '_cols++;printf("#X %gKohm (%gC)\\n",TEMP_SP,DEGC_SP)'
    
    The supplied macro alters this slightly (replacing %g with %f)
    and uses the :meth:`spec2nexus.scanf.scanf` implementation with this format::
    
        fmt = "#X %fKohm (%fC)"
        
    Depending on the circumstances, this might be a good candidate to override
    with a custom *ControlLineHandler* that parses the data as written.
    If the conversion process fails for any reason in this implementation, the *#X* line is ignored.
    
    IN-MEMORY REPRESENTATION
    
    * (SpecDataFileScan): **TEMP_SP**
    * (SpecDataFileScan): **DEGC_SP**
    
    HDF5/NeXus REPRESENTATION
    
    * Dataset named **TEMP_SP** in the *NXentry* group, such as */S1/TEMP_SP*
    * Dataset named **DEGC_SP** in the *NXentry* group, such as */S1/DEGC_SP*
    '''

    key = '#X'
    # TODO: Needs an example data file to test
    
    def process(self, text, scan, *args, **kws):
        fmt = "#X %fKohm (%fC)"
        try:
            # This looks fragile!
            scan.TEMP_SP, scan.DEGC_SP = scanf(fmt, text)
            scan.addH5writer(self.key, self.writer)
        except:
            pass
    
    def writer(self, h5parent, writer, scan, nxclass=None, *args, **kws):
        '''Describe how to store this data in an HDF5 NeXus file'''
        # consider putting this info under NXsample or NXentry/metadata
        if hasattr('TEMP_SP', scan):
            write_dataset(h5parent, "TEMP_SP", scan.TEMP_SP, description='temperature set point')
        if hasattr('DEGC_SP', scan):
            write_dataset(h5parent, "DEGC_SP", scan.DEGC_SP, units='C', description='temperature set point (C)')


class SPEC_DataLine(ControlLineHandler):
    '''
    **(scan data)** -- scan data line
    
    Scan data could include interspersed MCA data or
    even describe 2-D or 3-D data.  T
    his method reads the data lines and
    buffers them for post-processing in 
    :meth:`spec2nexus.plugins.spec_common_spec2nexus.data_lines_postprocessing`.
    
    IN-MEMORY REPRESENTATION
    
    * (SpecDataFileScan): **data_lines** : values
    * (SpecDataFileScan): **data** : {labels: values}
    
    HDF5/NeXus REPRESENTATION
    
    * *NXdata* group named **data** in the *NXentry* group, such as */S1/data*
      
      * datasets with names supplied in **L**, array values collected in **data_lines**

    '''

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
    **#@MCA** -- MCA data formatting declaration (ignored for now)
    
    declares this scan contains MCA data (SPEC's array_dump() format, such as ``"#@MCA 16C"``)
    
    From documentation provided by the ESRF BLISS group: 
    (http://www.esrf.eu/blissdb/macros/getsource.py?macname=mca.mac)
    
        #@MCA 16C 
        Format string passed to data_dump() function. 
        This format string is held by the global variable "MCA_FMT" and can then been adapted to particular needs. 
        "%%16C" is the default. It dumps data on 1 line, cut every 16 points::
        
            @A 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\\
             0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\\
             0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\\
             0 0 0 0 0 0 0 0 0 0 0 ...
        
        "%%16" would do the same without any backslash
        "1" would dump 1 point per line, ...

    '''

    key = '#@MCA'
    
    def process(self, text, scan, *args, **kws):
        # #@MCA 16C
        # Isn't this only informative to how the data is presented in the file?
        pass        # not sure how to handle this, ignore it for now


class SPEC_MCA_Array(ControlLineHandler):
    '''
    **@A** -- MCA Array data
    
    MCA data. Each value is the content of one channel, or an 
    integrated value over several channels if a reduction was applied.

    Since the MCA Array data is interspersed with scan data, 
    this method reads the data lines and buffers them for post-processing in 
    :meth:`spec2nexus.plugins.spec_common_spec2nexus.data_lines_postprocessing`.
    
    IN-MEMORY REPRESENTATION
    
    * (SpecDataFileScan): **data_lines** : values
    * (SpecDataFileScan): **data** : {labels: values}
    
    HDF5/NeXus REPRESENTATION
    
    * *NXdata* group named **data** in the *NXentry* group, such as */S1/data*
      
      * Dataset **_mca_** : *float* MCA data reported on *@A* lines
      * Dataset **_mca_channel_**: provided as HDF5 dimension scale for **_mca_** dataset
          * if CALIB data specified: *float* scaled MCA channels -- :math:`x_k = a +bk + ck^2`
          * if CALIB data not specified: *int* MCA channel numbers

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
    '''
    **#@CALIB** -- coefficients to compute a scale based on the MCA channel number
    
    :math:`x_k = a +bk + ck^2` for MCA data, :math:`k` is channel number
    
    IN-MEMORY REPRESENTATION
    
    * (SpecDataFileScan): **MCA['CALIB']** = ``dict(a, b, c)``
    
    HDF5/NeXus REPRESENTATION
    
    * defines a dimension scale for MCA data
    * *NXcollection* group named **MCA** in the *NXentry* group, such as */S1/MCA*
      
      * Dataset **calib_a** : *float*
      * Dataset **calib_b** : *float*
      * Dataset **calib_c** : *float*

    '''

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
        scan.addH5writer(self.key, self.writer)
    
    def writer(self, h5parent, writer, scan, nxclass=None, *args, **kws):
        '''Describe how to store this data in an HDF5 NeXus file'''
        if hasattr('MCA', scan):
            if 'CALIB' in scan.MCA:
                mca_group = openGroup(h5parent, 'MCA', nxclass, description='MCA metadata')
                calib_dict = scan.MCA['CALIB']
                for key in ('a b c'.split()):
                    if key in calib_dict:
                        write_dataset(mca_group, 'calib_' + key, calib_dict[key])


class SPEC_MCA_ChannelInformation(ControlLineHandler):
    '''
    **#@CHANN** -- MCA channel information 
    
    number_saved, first_saved, last_saved, reduction_coef
    
    IN-MEMORY REPRESENTATION
    
    * (SpecDataFileScan): **MCA['CALIB']** = ``dict(number_saved, first_saved, last_saved, reduction_coef)``
    
    HDF5/NeXus REPRESENTATION
    
    * *NXcollection* group named **MCA** in the *NXentry* group, such as */S1/MCA*
      
      * Dataset **number_saved** : *int* number of channels saved
      * Dataset **first_saved** : *int* first channel saved
      * Dataset **first_saved** : *int* last channel saved
      * Dataset **reduction_coef** : *float* reduction coefficient

    '''

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
        scan.addH5writer(self.key, self.writer)
    
    def writer(self, h5parent, writer, scan, nxclass=None, *args, **kws):
        '''Describe how to store this data in an HDF5 NeXus file'''
        if hasattr('MCA', scan):
            mca_group = openGroup(h5parent, 'MCA', nxclass, description='MCA metadata')
            mca = scan.MCA
            for key in ('number_saved  first_saved  last_saved  reduction_coef'.split()):
                if key in mca:
                    write_dataset(mca_group, key, mca[key])


class SPEC_MCA_CountTime(ControlLineHandler):
    '''
    **#@CTIME** -- MCA count times
    
    preset_time, elapsed_live_time, elapsed_real_time
    
    IN-MEMORY REPRESENTATION
    
    * (SpecDataFileScan): **MCA['CALIB']** = ``dict(preset_time, elapsed_live_time, elapsed_real_time)``
    
    HDF5/NeXus REPRESENTATION
    
    * *NXcollection* group named **MCA** in the *NXentry* group, such as */S1/MCA*
      
      * Dataset **preset_time** : *float*
      * Dataset **elapsed_live_time** : *float*
      * Dataset **elapsed_real_time** : *float*

    '''

    key = '#@CTIME'
    
    def process(self, text, scan, *args, **kws):
        s = strip_first_word(text).split()
        preset_time, elapsed_live_time, elapsed_real_time = map(float, s)

        if not hasattr(scan, 'MCA'):
            scan.MCA = {}

        scan.MCA['preset_time'] = preset_time
        scan.MCA['elapsed_live_time'] = elapsed_live_time
        scan.MCA['elapsed_real_time'] = elapsed_real_time
        scan.addH5writer(self.key, self.writer)
    
    def writer(self, h5parent, writer, scan, nxclass=None, *args, **kws):
        '''Describe how to store this data in an HDF5 NeXus file'''
        if hasattr('MCA', scan):
            mca_group = openGroup(h5parent, 'MCA', nxclass, description='MCA metadata')
            mca = scan.MCA
            for key in ('preset_time  elapsed_live_time  elapsed_real_time'.split()):
                if key in mca:
                    write_dataset(mca_group, key, mca[key], units='s')


class SPEC_MCA_RegionOfInterest(ControlLineHandler):
    '''
    **#@ROI** -- MCA ROI (Region Of Interest) channel information
    
    ROI_name, first_chan, last_chan
    
    IN-MEMORY REPRESENTATION
    
    * (SpecDataFileScan): **MCA['ROI']** = {ROI_name:dict(first_chan, last_chan)}
    
    HDF5/NeXus REPRESENTATION
    
    * *NXcollection* group **ROI** in 
      in *NXcollection* group named **MCA** 
      in the *NXentry* group, such as */S1/MCA/ROI*
      
      * Dataset **{ROI_name}** : *int* [first_chan, last_chan]

    '''

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
    
    def writer(self, h5parent, writer, scan, nxclass=None, *args, **kws):
        '''Describe how to store this data in an HDF5 NeXus file'''
        if hasattr('MCA', scan):
            if hasattr('ROI', scan.MCA):
                mca_group = openGroup(h5parent, 'MCA', nxclass, description='MCA metadata')
                roi_group = openGroup(mca_group, 'ROI', nxclass, description='Regions Of Interest')
                roi_dict = scan.MCA['ROI']
                for key, roi in roi_dict.items():
                    dataset = [roi['first_chan'], roi['last_chan']]
                    desc = 'first_chan, last_chan'
                    write_dataset(roi_group, key, dataset, description=desc, units='channel')

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
    scan.addH5writer('scan data', data_lines_writer)


def data_lines_writer(h5parent, writer, scan, *args, **kws):
    '''Describe how to store scan data in an HDF5 NeXus file'''
    desc = 'SPEC scan data'
    nxdata = makeGroup(h5parent, 'data', 'NXdata', description=desc)
    writer.save_data(nxdata, scan)
