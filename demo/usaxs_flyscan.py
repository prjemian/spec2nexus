#!/usr/bin/env python

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
Plot data from the USAXS FlyScan macro

.. autosummary::

    ~read_reduced_fly_scan_file
    ~retrieve_flyScanData
    ~USAXS_FlyScan_Structure
    ~USAXS_FlyScan_Plotter

'''

import h5py
import numpy
import os

import spec2nexus.specplot
import spec2nexus.specplot_gallery


# methods picked (& modified) from the USAXS livedata project
def read_reduced_fly_scan_file(hdf5_file_name):
    '''
    read any and all reduced data from the HDF5 file, return in a dictionary
    
    dictionary = {
      'full': dict(Q, R, R_max, ar, fwhm, centroid)
      '250':  dict(Q, R, dR)
      '5000': dict(Q, R, dR)
    }
    '''

    reduced = {}
    hdf = h5py.File(hdf5_file_name, 'r')
    entry = hdf['/entry']
    for key in entry.keys():
        if key.startswith('flyScan_reduced_'):
            nxdata = entry[key]
            d = {}
            for dsname in ['Q', 'R']:
                if dsname in nxdata:
                    value = nxdata[dsname]
                    if value.size == 1:
                        d[dsname] = float(value[0])
                    else:
                        d[dsname] = numpy.array(value)
            reduced[key[len('flyScan_reduced_'):]] = d
    hdf.close()
    return reduced


# $URL: https://subversion.xray.aps.anl.gov/small_angle/USAXS/livedata/specplot.py $
REDUCED_FLY_SCAN_BINS   = 250       # the default
def retrieve_flyScanData(scan):
    '''retrieve reduced, rebinned data from USAXS Fly Scans'''
    path = os.path.dirname(scan.header.parent.fileName)
    key_string = 'FlyScan file name = '
    comment = scan.comments[2]
    index = comment.find(key_string) + len(key_string)
    hdf_file_name = comment[index:-1]
    abs_file = os.path.abspath(os.path.join(path, hdf_file_name))

    plotData = {}
    if os.path.exists(abs_file):
        reduced = read_reduced_fly_scan_file(abs_file)
        s_num_bins = str(REDUCED_FLY_SCAN_BINS)

        choice = reduced.get(s_num_bins) or reduced.get('full')

        if choice is not None:
            plotData = {axis: choice[axis] for axis in 'Q R'.split()}

    return plotData


class USAXS_FlyScan_Plotter(spec2nexus.specplot.LinePlotter):
    '''
    customize `FlyScan` handling, plot :math:`log(I)` *vs.* :math:`log(Q)`
    
    The USAXS FlyScan data is stored in a NeXus HDF5 file in a subdirectory
    below the SPEC data file.  This code uses existing code from the
    USAXS instrument to read that file.
    '''
    
    def retrieve_plot_data(self):
        '''retrieve reduced data from the FlyScan's HDF5 file'''
        # get the data from the HDF5 file
        fly_data = retrieve_flyScanData(self.scan)
        
        if len(fly_data) != 2:
            raise spec2nexus.specplot.NoDataToPlot(str(self.scan))

        self.signal = 'R'
        self.axes = ['Q',]
        self.data = fly_data

        # customize the plot just a bit
        # sample name as given by the user?
        subtitle = '#' + str(self.scan.scanNum)
        subtitle += ' FlyScan: ' + self.scan.comments[0]
        self.set_plot_subtitle(subtitle)
        self.set_x_log(True)
        self.set_y_log(True)
        self.set_x_title(r'$|\vec{Q}|, 1/\AA$')
        self.set_y_title(r'USAXS $R(|\vec{Q}|)$, a.u.')
    
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


def debugging_setup():
    import sys
    import shutil
    sys.path.insert(0, os.path.join('..', 'src'))
    path = '__usaxs__'
    shutil.rmtree(path, ignore_errors=True)
    os.mkdir(path)
    sys.argv.append('-d')
    sys.argv.append(path)
    sys.argv.append(os.path.join('..', 'src', 'spec2nexus', 'data', '02_03_setup.dat'))


def main():
    selector = spec2nexus.specplot.Selector()
    selector.add('FlyScan', USAXS_FlyScan_Plotter)
    spec2nexus.specplot_gallery.main()


if __name__ == '__main__':
    # debugging_setup()
    main()
