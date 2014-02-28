#!/usr/bin/env python 
# -*- coding: utf-8 -*-

#-----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
#-----------------------------------------------------------------------------


'''Parses SPEC data using nexpy.api.nexus.tree API (for NeXpy project)'''


import numpy as np
from nexpy.api.nexus import NXroot, NXentry, NXfield, NXdata, NXlog
import spec2nexus


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class Parser(object):
    ''' '''
    
    def __init__(self, spec_data):
        self.SPECfile = spec_data
    
    def toTree(self, scan_list=[]):
        '''
        convert scans from chosen SPEC file into NXroot object and structure
        
        called from nexpy.readers.readspec.ImportDialog.get_data__prjPySpec() after clicking <Ok> in dialog
        
        Each scan in the range from self.scanmin to self.scanmax (inclusive)
        will be converted to a NXentry.  Scan data will go in a NXdata where 
        the signal=1 is the last column and the corresponding axes= is the first column.
        
        :param [int] scanlist
        :raises: ValueError is Min or Max scan number are not given properly
        '''
        # check that scan_list is valid
        if len(scan_list) == 0:
            return None
        
        complete_scan_list = self.SPECfile.scans.keys()
        for key in scan_list:
            if key not in complete_scan_list:
                msg = 'scan ' + str(key) + ' was not found'
                raise ValueError, msg
        
        root = NXroot()

        root.attrs['prjPySpec_version'] = spec2nexus.__version__
        header0 = self.SPECfile.headers[0]
        root.attrs['SPEC_file'] = header0.file
        root.attrs['SPEC_epoch'] = header0.epoch
        root.attrs['SPEC_date'] = spec2nexus.iso8601(header0.date)
        root.attrs['SPEC_comments'] = '\n'.join(header0.comments)
        try:
            c = header0.comments[0]
            user = c[c.find('User = '):].split('=')[1].strip()
            root.attrs['SPEC_user'] = user
        except:
            pass
        root.attrs['SPEC_num_headers'] = len(self.SPECfile.headers)

        for key in scan_list:
            scan = self.SPECfile.getScan(key)
            entry = NXentry()
            entry.title = str(scan)
            entry.date = spec2nexus.iso8601(scan.date)  
            entry.command = scan.scanCmd 
            entry.scan_number = NXfield(scan.scanNum)
            entry.comments = '\n'.join(scan.comments)
            entry.data = self.scan_NXdata(scan)            # store the scan data
            entry.positioners = self.metadata_NXlog(scan.positioner, 
                                                    'SPEC positioners (#P & #O lines)')
            if len(scan.metadata) > 0:
                entry.metadata = self.metadata_NXlog(scan.metadata, 
                                                     'SPEC metadata (UNICAT-style #H & #V lines)')

            if len(scan.G) > 0:
                entry.G = NXlog()
                desc = "SPEC geometry arrays, meanings defined by SPEC diffractometer support"
                # e.g.: SPECD/four.mac
                # http://certif.com/spec_manual/fourc_4_9.html
                entry.G.attrs['description'] = desc
                for item, value in scan.G.items():
                    entry.G[item] = NXfield(map(float, value.split()))
            if scan.T != '':
                entry['counting_basis'] = NXfield('SPEC scan with constant counting time')
                entry['T'] = NXfield(float(scan.T))
                entry['T'].units = 'seconds'
                entry['T'].description = 'SPEC scan with constant counting time'
            elif scan.M != '':
                entry['counting_basis'] = NXfield('SPEC scan with constant monitor count')
                entry['M'] = NXfield(float(scan.M))
                entry['M'].units = 'counts'
                entry['M'].description = 'SPEC scan with constant monitor count'
            if scan.Q != '':
                entry['Q'] = NXfield(map(float,scan.Q.split()))
                entry['Q'].description = 'hkl at start of scan'

            root['scan_' + str(key)] = entry
        return root
    
    def scan_NXdata(self, scan):
        '''
        return the scan data in an NXdata object
        '''
        nxdata = NXdata()
        nxdata.attrs['description'] = 'SPEC scan data'
        
        scan_type = scan.scanCmd.split()[0]
        if scan_type in ('mesh', 'hklmesh'):
            # hklmesh  H 1.9 2.1 100  K 1.9 2.1 100  -800000
            self.parser_mesh(nxdata, scan)
        elif scan_type in ('hscan', 'kscan', 'lscan', 'hklscan'):
            # hklscan  1.00133 1.00133  1.00133 1.00133  2.85 3.05  200 -400000
            h_0, h_N, k_0, k_N, l_0, l_N = scan.scanCmd.split()[1:7]
            if   h_0 != h_N: axis = 'H'
            elif k_0 != k_N: axis = 'K'
            elif l_0 != l_N: axis = 'L'
            self.parser_1D_columns(nxdata, scan)
            nxdata.nxaxes = nxdata[axis]
        else:
            self.parser_1D_columns(nxdata, scan)

        # these locations suggested to NIAC, easier to parse than attached to dataset!
        nxdata.attrs['signal'] = nxdata.nxsignal.nxname         
        nxdata.attrs['axes'] = ':'.join([obj.nxname for obj in nxdata.nxaxes])
        
        return nxdata
    
    def parser_1D_columns(self, nxdata, scan):
        '''generic data parser for 1-D column data'''
        for column in scan.L:
            clean_name = spec2nexus.sanitize_name(nxdata, column)
            nxdata[clean_name] = NXfield(scan.data[column])
            nxdata[clean_name].original_name = column

        signal = spec2nexus.sanitize_name(nxdata, scan.column_last)      # primary Y axis
        axis = spec2nexus.sanitize_name(nxdata, scan.column_first)       # primary X axis
        nxdata.nxsignal = nxdata[signal]
        nxdata.nxaxes = nxdata[axis]
        
        self.parser_mca_spectra(nxdata, scan, axis)
    
    def parser_mca_spectra(self, nxdata, scan, primary_axis_label):
        '''parse for optional MCA spectra'''
        if '_mca_' in scan.data:        # check for it
            nxdata.mca__spectrum_ = NXfield(scan.data['_mca_'])
            nxdata.mca__spectrum_channel = NXfield(range(1, len(scan.data['_mca_'][0])+1))
            nxdata.mca__spectrum_channel.units = 'channel'
            axes = (primary_axis_label, 'mca__spectrum_channel')
            nxdata.mca__spectrum_.axes = ':'.join( axes )
    
    def parser_mesh(self, nxdata, scan):
        '''data parser for 2-D mesh and hklmesh'''
        # 2-D parser: http://www.certif.com/spec_help/mesh.html
        # mesh motor1 start1 end1 intervals1 motor2 start2 end2 intervals2 time
        # 2-D parser: http://www.certif.com/spec_help/hklmesh.html
        #  hklmesh Q1 start1 end1 intervals1 Q2 start2 end2 intervals2 time
        # mesh:    nexpy/examples/33id_spec.dat  scan 22
        # hklmesh: nexpy/examples/33bm_spec.dat  scan 17
        label1, start1, end1, intervals1, label2, start2, end2, intervals2, time = scan.scanCmd.split()[1:]
        if label1 not in scan.data:
            label1 = scan.L[0]      # mnemonic v. name
        if label2 not in scan.data:
            label2 = scan.L[1]      # mnemonic v. name
        axis1 = scan.data.get(label1)
        axis2 = scan.data.get(label2)
        intervals1, intervals2 = map(int, (intervals1, intervals2))
        start1, end1, start2, end2, time = map(float, (start1, end1, start2, end2, time))
        if len(axis1) < intervals1:     # stopped scan before second row started
            self.parser_1D_columns(nxdata, scan)        # fallback support
        else:
            axis1 = axis1[0:intervals1+1]
            axis2 = [axis2[row] for row in range(len(axis2)) if row % (intervals1+1) == 0]

            column_labels = scan.L
            column_labels.remove(label1)    # special handling
            column_labels.remove(label2)    # special handling
            if scan.scanCmd.startswith('hkl'):
                # find the reciprocal space axis held constant
                label3 = [key for key in ('H', 'K', 'L') if key not in (label1, label2)][0]
                axis3 = scan.data.get(label3)[0]
                nxdata[label3] = NXfield(axis3)
                column_labels.remove(label3)    # already handled

            nxdata[label1] = NXfield(axis1)    # 1-D array
            nxdata[label2] = NXfield(axis2)    # 1-D array

            # build 2-D data objects (do not build label1, label2, [or label3] as 2-D objects)
            data_shape = [len(axis1), len(axis2)]
            for label in column_labels:
                axis = np.array( scan.data.get(label) )
                clean_name = spec2nexus.sanitize_name(nxdata, label)
                nxdata[clean_name] = NXfield(spec2nexus.reshape_data(axis, data_shape))
                nxdata[clean_name].original_name = label

            signal_axis_label = spec2nexus.sanitize_name(nxdata, scan.column_last)
            nxdata.nxsignal = nxdata[signal_axis_label]
            nxdata.nxaxes = [nxdata[label1], nxdata[label2]]

        if '_mca_' in scan.data:    # 3-D array
            # TODO: ?merge with parser_mca_spectra()?
            num_channels = len(scan.data['_mca_'][0])
            data_shape.append(num_channels)
            mca = np.array(scan.data['_mca_'])
            nxdata.mca__spectrum_ = NXfield(spec2nexus.reshape_data(mca, data_shape))
            nxdata.mca__spectrum_channel = NXfield(range(1, num_channels+1))
            nxdata.mca__spectrum_channel.units = 'channel'
            axes = (label1, label2, 'mca__spectrum_channel')
            nxdata.mca__spectrum_.axes = ':'.join( axes )
    
    def metadata_NXlog(self, spec_metadata, description):
        '''
        return the specific metadata in an NXlog object
        '''
        nxlog = NXlog()
        nxlog.attrs['description'] = description
        for subkey, value in spec_metadata.items():
            clean_name = spec2nexus.sanitize_name(nxlog, subkey)
            nxlog[clean_name] = NXfield(value)
            nxlog[clean_name].original_name = subkey
        return nxlog
