#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014-2017, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
#-----------------------------------------------------------------------------


'''
Shape scan data from raw to different dimensionality

Some SPEC macros collect data in a mesh or grid yet 
report the data as a 1-D sequence of observations.
For further processing (such as plotting), the scan data
needs to be reshaped according to its intended dimensionality.
'''


import numpy
import spec
import utils


def reshape_data(scan_data, scan_shape):
    '''modified from nexpy.readers.readspec.reshape_data'''
    scan_size = numpy.prod(scan_shape)
    if scan_data.size == scan_size:
        data = scan_data
    elif scan_data.size < scan_size:
        data = numpy.empty(scan_size)
        data.fill(numpy.NaN)               # pad data with NaN
        data[0:scan_data.size] = scan_data.ravel()  # flatten & insert
    else:
        data = scan_data.ravel()        # flatten
        data = data[0:scan_size]        # truncate extra data
    return data.reshape(scan_shape)


class MeshStructure(object):
    '''
    container for data from a mesh or hklmesh scan
    '''
    
    def __init__(self):
        self.signal = None
        self.axes = []
        self.labels = []

    def mesh(self, scan):
        '''
        data parser for 2-D mesh and hklmesh
        '''
        # 2-D parser: http://www.certif.com/spec_help/mesh.html
        # mesh motor1 start1 end1 intervals1 motor2 start2 end2 intervals2 time
        # 2-D parser: http://www.certif.com/spec_help/hklmesh.html
        #  hklmesh Q1 start1 end1 intervals1 Q2 start2 end2 intervals2 time
        # mesh:    data/33id_spec.dat  scan 22
        # hklmesh: data/33bm_spec.dat  scan 17
        
        assert(isinstance(scan, spec.SpecDataFileScan))
        
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
            # TODO: fallback to 1-D support
            pass
        else:
            axis1 = axis1[0:intervals1+1]
            self.labels.append(label1)
            self.axes.append(axis1)    # 1-D array

            axis2 = [axis2[row] for row in range(len(axis2)) if row % (intervals1+1) == 0]
            self.labels.append(label2)
            self.axes.append(axis2)    # 1-D array
    
            column_labels = scan.L
            column_labels.remove(label1)    # special handling
            column_labels.remove(label2)    # special handling
            if scan.scanCmd.startswith('hkl'):
                # find the reciprocal space axis held constant
                label3 = [key for key in ('H', 'K', 'L') if key not in (label1, label2)][0]
                axis3 = scan.data.get(label3)[0]
                self.labels.append(label3)
                self.axes.append(axis3)    # constant
    
            # build 2-D data objects (do not build label1, label2, [or label3] as 2-D objects)
            data_shape = [len(axis1), len(axis2)]
            for label in column_labels:
                if label not in nxdata:
                    axis = numpy.array( scan.data.get(label) )
                    __ = reshape_data(axis, data_shape) # TODO: do something with this
                    # self.write_ds(nxdata, label, utils.reshape_data(axis, data_shape))
                else:
                    pass
    
            self.signal = utils.clean_name(scan.column_last)
            axes = ':'.join([label1, label2])
    
        if '_mca_' in scan.data:    # 3-D array(s)
            # save each spectrum
            for key, spectrum in sorted(scan.data['_mca_'].items()):
                num_channels = len(spectrum[0])
                data_shape.append(num_channels)
                mca = numpy.array(spectrum)
                data = reshape_data(mca, data_shape)
                channels = range(1, num_channels+1)
                ds_name = '_' + key + '_'
                # self.write_ds(nxdata, ds_name, data, axes=axes+':'+ds_name+'channel_', units='counts')
                # self.write_ds(nxdata, ds_name+'channel_', channels, units='channel')
    
        #return signal, axes    # not necessary
