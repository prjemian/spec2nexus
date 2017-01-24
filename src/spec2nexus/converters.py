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

.. autosummary::

    ~reshape_data
    ~PlotDataStructure
    ~XYStructure
    ~MeshStructure
    ~NoDataToPlot
    ~HandleMeshDataAs1D

'''


import numpy
import spec
import utils
import spec2nexus.spec

class NoDataToPlot(KeyError): 
    'scan aborted before any points gathered or data not present in SPEC file'
    pass

class HandleMeshDataAs1D(RuntimeWarning): 
    'mesh scan aborted before second row started can plot as 1-D'
    pass


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


class PlotDataStructure(object):
    '''
    base class: describe plottable data
    
    :param obj scan: instance of :class:`spec2nexus.spec.SpecDataFileScan`
    
    Attributes:
    
    :signal: name of the 'signal' data (default data to be plotted)
    :data: values of various collected arrays {label: array}
    :axes: names of the axes of signal data
    
    Re-implement the :meth:`plottable()` method in each subclass to
    report if the data can be plotted.
    '''
    
    def __init__(self, scan):
        assert(isinstance(scan, (spec.SpecDataFileScan,spec2nexus.spec.SpecDataFileScan)))
        self.signal = None
        self.axes = []
        self.data = {}
    
    def plottable(self):
        '''
        can this data be plotted as expected?
        '''
        return False    # override in subclass with specific tests


class XYStructure(PlotDataStructure):
    '''
    describe plottable data from 1-D scans such as `ascan`
    
    :param obj scan: instance of :class:`spec2nexus.spec.SpecDataFileScan`
    
    Attributes:
    
    :x: array of horizontal axis values
    :y: array of vertical axis values
    '''
    
    def __init__(self, scan):
        PlotDataStructure.__init__(self, scan)

        # plot last column v. first column
        self.signal = scan.column_last
        if self.signal not in scan.data:
            raise NoDataToPlot(str(scan))
        self.axes = [scan.column_first,]
        self.data = {label: scan.data.get(label) for label in scan.L}
    
    def plottable(self):
        '''
        can this data be plotted as expected?
        '''
        if self.signal in self.data:
            signal = self.data[self.signal]
            if signal is not None and len(signal) > 0 and len(self.axes) == 1:
                if len(signal) == len(self.data[self.axes[0]]):
                    return True
        return False


class MeshStructure(PlotDataStructure):
    '''
    describe plottable data from a *mesh* or *hklmesh* scan
    
    :param obj scan: instance of :class:`spec2nexus.spec.SpecDataFileScan`
    
    References:
    
    :mesh 2-D parser: http://www.certif.com/spec_help/mesh.html
        
        ::
        
            mesh motor1 start1 end1 intervals1 motor2 start2 end2 intervals2 time
    
    :hklmesh 2-D parser: http://www.certif.com/spec_help/hklmesh.html
        
        ::
        
            hklmesh Q1 start1 end1 intervals1 Q2 start2 end2 intervals2 time
     
    '''
    
    def __init__(self, scan):
        PlotDataStructure.__init__(self, scan)
        self._mesh_(scan)

    def _mesh_(self, scan):
        '''
        data parser for 2-D mesh and hklmesh
        '''
        label1, start1, end1, intervals1, label2, start2, end2, intervals2, time = scan.scanCmd.split()[1:]
        if label1 not in scan.data:
            label1 = scan.L[0]      # mnemonic v. name
        if label2 not in scan.data:
            label2 = scan.L[1]      # mnemonic v. name
        axis1 = scan.data.get(label1)
        axis2 = scan.data.get(label2)
        intervals1, intervals2 = map(int, (intervals1, intervals2))
        start1, end1, start2, end2, time = map(float, (start1, end1, start2, end2, time))

        if len(axis1) < intervals1 and min(axis2) == max(axis2):
            # stopped scan before second row started, 1-D plot is better (issue #82)
            msg = 'stopped scan before second row started'
            msg += ', fall back to 1-D plot'
            raise HandleMeshDataAs1D(msg)

        axis1 = axis1[0:intervals1+1]
        self.data[label1] = axis1    # 1-D array

        axis2 = [axis2[row] for row in range(len(axis2)) if row % (intervals1+1) == 0]
        self.data[label2] = axis2    # 1-D array

        column_labels = scan.L
        column_labels.remove(label1)    # special handling
        column_labels.remove(label2)    # special handling
        if scan.scanCmd.startswith('hkl'):
            # find the reciprocal space axis held constant
            label3 = [key for key in ('H', 'K', 'L') if key not in (label1, label2)][0]
            axis3 = scan.data.get(label3)[0]
            self.data[label3] = axis3    # constant

        # build 2-D data objects (do not build label1, label2, [or label3] as 2-D objects)
        data_shape = [len(axis2), len(axis1)]
        for label in column_labels:
            if label not in self.data:
                axis = numpy.array( scan.data.get(label) )
                self.data[label] = reshape_data(axis, data_shape)
            else:
                pass

        self.signal = utils.clean_name(scan.column_last)
        self.axes = [label1, label2]
    
        if spec.MCA_DATA_KEY in scan.data:    # 3-D array(s)
            # save each spectrum
            for key, spectrum in sorted(scan.data[spec.MCA_DATA_KEY].items()):
                num_channels = len(spectrum[0])
                data_shape.append(num_channels)
                mca = numpy.array(spectrum)
                data = reshape_data(mca, data_shape)
                channels = range(1, num_channels+1)
                ds_name = '_' + key + '_'
                self.data[ds_name] = data
                self.data[ds_name+'channel_'] = channels
    
    def plottable(self):
        '''
        can this data be plotted as expected?
        '''
        if self.signal in self.data:
            signal = self.data[self.signal]
            for axis in self.axes:
                if axis not in self.data:
                    break
            axis_shape = [len(axis) for axis in self.axes]
            # TODO: compare axis_shape with signal_shape
            return True
        return False
