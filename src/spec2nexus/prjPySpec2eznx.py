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


'''Parses SPEC data using spec2nexus.eznx API (only requires h5py)'''


import numpy as np
import eznx
import spec2nexus


# see: http://download.nexusformat.org/doc/html/classes/base_classes/index.html
#CONTAINER_CLASS = 'NXlog'          # information that is recorded against time
#CONTAINER_CLASS = 'NXnote'         # store additional information in a NeXus file
#CONTAINER_CLASS = 'NXparameters'   # Container for parameters, usually used in processing or analysis
CONTAINER_CLASS = 'NXcollection'    # Use NXcollection to gather together any set of terms
        

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class Writer(object):
    '''
    writes out scans from SPEC data file to NeXus HDF5 file
    
    :param obj spec_data: instance of :class:`~spec2nexus.prjPySpec.SpecDataFile`
    '''

    def __init__(self, spec_data):
        self.spec = spec_data
        
    def save(self, hdf_file, scan_list=[]):
        '''
        save the information in this SPEC data file to a NeXus HDF5 file
        
        Each scan in scan_list will be converted to a NXentry.  
        Scan data will go in a NXdata where the signal=1 is the 
        last column and the corresponding axes= is the name of 
        the first column.
        
        :param str hdf_file: name of NeXus/HDF5 file to be written
        :param [int] scanlist: list of scan numbers to be read
        '''
        root = eznx.makeFile(hdf_file, **self.root_attributes())
        for key in scan_list:
            nxentry = eznx.makeGroup(root, 'S'+str(key), 'NXentry')
            self.save_scan(nxentry, self.spec.getScan(key))
        root.close()    # be CERTAIN to close the file
    
    def root_attributes(self):
        '''*internal*: returns the attributes to be written to the root element as a dict'''
        header0 = self.spec.headers[0]
        dd = dict(
            prjPySpec_version = spec2nexus.__version__,
            SPEC_file = header0.file,
            SPEC_epoch = header0.epoch,
            SPEC_date = spec2nexus.iso8601(header0.date),
            SPEC_comments = '\n'.join(header0.comments),
            SPEC_num_headers = len(self.spec.headers),
            )
        try:
            c = header0.comments[0]
            user = c[c.find('User = '):].split('=')[1].strip()
            dd['SPEC_user'] = user
        except:
            pass
        return dd
    
    def save_scan(self, nxentry, scan):
        '''*internal*: save the data from each SPEC scan to its own NXentry group'''
        eznx.write_dataset(nxentry, "title", str(scan))
        eznx.write_dataset(nxentry, "scan_number", scan.scanNum)
        eznx.write_dataset(nxentry, "date", spec2nexus.iso8601(scan.date)  )
        eznx.write_dataset(nxentry, "command", scan.scanCmd)
        eznx.write_dataset(nxentry, "scan_number", scan.scanNum)
        eznx.write_dataset(nxentry, "comments", '\n'.join(scan.comments))

        desc = 'SPEC scan data'
        nxdata = eznx.makeGroup(nxentry, 'data', 'NXdata', description=desc)
        self.save_data(nxdata, scan)
        
        desc='SPEC positioners (#P & #O lines)'
        group = eznx.makeGroup(nxentry, 'positioners', CONTAINER_CLASS, description=desc)
        self.save_dict(group, scan.positioner)

        if len(scan.metadata) > 0:
            desc='SPEC metadata (UNICAT-style #H & #V lines)'
            group = eznx.makeGroup(nxentry, 'metadata', CONTAINER_CLASS, description=desc)
            self.save_dict(group, scan.metadata)

        if len(scan.G) > 0:
            # e.g.: SPECD/four.mac
            # http://certif.com/spec_manual/fourc_4_9.html
            desc = "SPEC geometry arrays, meanings defined by SPEC diffractometer support"
            group = eznx.makeGroup(nxentry, 'G', CONTAINER_CLASS, description=desc)
            dd = {}
            for item, value in scan.G.items():
                dd[item] = map(float, value.split())
            self.save_dict(group, dd)

        if scan.T != '':
            desc = 'SPEC scan with constant counting time'
            eznx.write_dataset(nxentry, "counting_basis", desc)
            eznx.write_dataset(nxentry, "T", float(scan.T), units='s', description = desc)
        elif scan.M != '':
            desc = 'SPEC scan with constant monitor count'
            eznx.write_dataset(nxentry, "counting_basis", desc)
            eznx.write_dataset(nxentry, "M", float(scan.M), units='counts', description = desc)

        if scan.Q != '':
            desc = 'hkl at start of scan'
            eznx.write_dataset(nxentry, "Q", map(float,scan.Q.split()), description = desc)

    def save_dict(self, group, data):
        '''*internal*: store a dictionary'''
        for k, v in data.items():
            self.write_ds(group, k, v)

    def save_data(self, nxdata, scan):
        '''*internal*: store the scan data'''
        scan_type = scan.scanCmd.split()[0]

        signal, axes = '', ['',]
        if scan_type in ('mesh', 'hklmesh'):
            # hklmesh  H 1.9 2.1 100  K 1.9 2.1 100  -800000
            signal, axes = self.mesh(nxdata, scan)
        elif scan_type in ('hscan', 'kscan', 'lscan', 'hklscan'):
            # hklscan  1.00133 1.00133  1.00133 1.00133  2.85 3.05  200 -400000
            h_0, h_N, k_0, k_N, l_0, l_N = scan.scanCmd.split()[1:7]
            if   h_0 != h_N: axes = ['H',]
            elif k_0 != k_N: axes = ['K',]
            elif l_0 != l_N: axes = ['L',]
            signal, axes = self.oneD(nxdata, scan)
        else:
            signal, axes = self.oneD(nxdata, scan)

        # these locations suggested to NIAC, easier to parse than attached to dataset!
        if len(signal) == 0:
            pass
        eznx.addAttributes(nxdata, signal=signal, axes=axes)
        eznx.addAttributes(nxdata[signal], signal=1, axes=axes)
    
    def oneD(self, nxdata, scan):
        '''*internal*: generic data parser for 1-D column data, returns signal and axis'''
        for column in scan.L:
            self.write_ds(nxdata, column, scan.data[column])

        signal = spec2nexus.clean_name(scan.column_last)      # primary Y axis
        axis = spec2nexus.clean_name(scan.column_first)       # primary X axis
        self.mca_spectra(nxdata, scan, axis)                 # records any MCA data
        return signal, axis
    
    def mca_spectra(self, nxdata, scan, primary_axis_label):
        '''*internal*: parse for optional MCA spectra'''
        if '_mca_' in scan.data:        # check for it
            axes = primary_axis_label + ':' + '_mca_channel_'
            channels = range(1, len(scan.data['_mca_'][0])+1)
            data = scan.data['_mca_']
            self.write_ds(nxdata, '_mca_', data, axes=axes)
            self.write_ds(nxdata, '_mca_channel_', channels, units = 'channel')
    
    def mesh(self, nxdata, scan):
        '''*internal*: data parser for 2-D mesh and hklmesh'''
        # 2-D parser: http://www.certif.com/spec_help/mesh.html
        # mesh motor1 start1 end1 intervals1 motor2 start2 end2 intervals2 time
        # 2-D parser: http://www.certif.com/spec_help/hklmesh.html
        #  hklmesh Q1 start1 end1 intervals1 Q2 start2 end2 intervals2 time
        # mesh:    data/33id_spec.dat  scan 22
        # hklmesh: data/33bm_spec.dat  scan 17
        signal, axes = '', ['',]
        
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
            signal, axes = self.oneD(nxdata, scan)        # fallback support
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
                self.write_ds(nxdata, label3, axis3)

            self.write_ds(nxdata, label1, axis1)    # 1-D array
            self.write_ds(nxdata, label2, axis2)    # 1-D array

            # build 2-D data objects (do not build label1, label2, [or label3] as 2-D objects)
            data_shape = [len(axis1), len(axis2)]
            for label in column_labels:
                axis = np.array( scan.data.get(label) )
                self.write_ds(nxdata, label, spec2nexus.reshape_data(axis, data_shape))

            signal = spec2nexus.clean_name(scan.column_last)
            axes = ':'.join([label1, label2])

        if '_mca_' in scan.data:    # 3-D array
            num_channels = len(scan.data['_mca_'][0])
            data_shape.append(num_channels)
            mca = np.array(scan.data['_mca_'])
            data = spec2nexus.reshape_data(mca, data_shape)
            channels = range(1, num_channels+1)
            self.write_ds(nxdata, '_mca_', data, axes=axes+':'+'_mca_channel_')
            self.write_ds(nxdata, '_mca_channel_', channels, units='channel')

        return signal, axes
    
    def write_ds(self, group, label, data, **attr):
        '''*internal*: writes a dataset to the HDF5 file, records the SPEC name as an attribute'''
        clean_name = spec2nexus.clean_name(label)
        eznx.write_dataset(group, clean_name, data, spec_name=label, **attr)
