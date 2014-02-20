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


'''Converts SPEC data files and scans into NeXus HDF5 files'''


import os                           #@UnusedImport
import re
import sys                          #@UnusedImport
import time
import numpy as np                  #@UnusedImport
from nexpy.api.nexus import NXroot, NXentry, NXfield, NXdata, NXlog

if __name__ == "__main__":
    # put us on the path for developers
    path = os.path.join('..', os.path.dirname(__file__))
    sys.path.insert(0, os.path.abspath(path))

import spec2nexus
import prjPySpec


hdf5_extension = '.hdf5'


class Parser(object):
    
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

        root.attrs['prjPySpec_version'] = prjPySpec.__version__
        header0 = self.SPECfile.headers[0]
        root.attrs['SPEC_file'] = header0.file
        root.attrs['SPEC_epoch'] = header0.epoch
        root.attrs['SPEC_date'] = iso8601(header0.date)
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
            entry.date = iso8601(scan.date)  
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
            clean_name = sanitize_name(nxdata, column)
            nxdata[clean_name] = NXfield(scan.data[column])
            nxdata[clean_name].original_name = column

        signal = sanitize_name(nxdata, scan.column_last)      # primary Y axis
        axis = sanitize_name(nxdata, scan.column_first)       # primary X axis
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
                clean_name = sanitize_name(nxdata, label)
                nxdata[clean_name] = NXfield(reshape_data(axis, data_shape))
                nxdata[clean_name].original_name = label

            signal_axis_label = sanitize_name(nxdata, scan.column_last)
            nxdata.nxsignal = nxdata[signal_axis_label]
            nxdata.nxaxes = [nxdata[label1], nxdata[label2]]

        if '_mca_' in scan.data:    # 3-D array
            # TODO: ?merge with parser_mca_spectra()?
            num_channels = len(scan.data['_mca_'][0])
            data_shape.append(num_channels)
            mca = np.array(scan.data['_mca_'])
            nxdata.mca__spectrum_ = NXfield(reshape_data(mca, data_shape))
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
            clean_name = sanitize_name(nxlog, subkey)
            nxlog[clean_name] = NXfield(value)
            nxlog[clean_name].original_name = subkey
        return nxlog


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def reshape_data(scan_data, scan_shape):
    # modified from nexpy.readers.readspec.reshape_data
    scan_size = np.prod(scan_shape)
    if scan_data.size == scan_size:
        data = scan_data
    elif scan_data.size < scan_size:
        data = np.empty(scan_size)
        data.fill(np.NaN)               # pad data with NaN
        data[0:scan_data.size] = scan_data.ravel()  # flatten & insert
    else:
        data = scan_data.ravel()        # flatten
        data = data[0:scan_size]        # truncate extra data
    return data.reshape(scan_shape)


def sanitize_name(group, key):
    # see: http://download.nexusformat.org/doc/html/datarules.html
    # clean name fits this regexp:  [A-Za-z_][\w_]*
    # easier:  [\w_]* but cannot start with a digit
    replacement = '_'
    noncompliance = '[^\w_]'
    txt = replacement.join(re.split(noncompliance, key)) # replace ALL non-compliances with '_'
    if txt[0].isdigit():
        txt = replacement + txt # can't start with a digit
    return txt


def iso8601(date):
    # parse time from SPEC (example: Wed Nov 03 13:39:34 2010)
    spec_fmt = '%a %b %d %H:%M:%S %Y'
    t = time.strptime(date, spec_fmt)
    # convert to ISO8601 format (example: 2010-11-03T13:39:34)
    iso_fmt = '%Y-%m-%dT%H:%M:%S'
    iso = time.strftime(iso_fmt, t)
    return iso


#-------------------------------------------------------------------------------------------


def developer_test():
    """
    test support for specific scans
    """
    spec_file_name = os.path.join('data', '33id_spec.dat')
    spec_data = prjPySpec.SpecDataFile(spec_file_name)
    scan = spec_data.getScan(22)
    print str(scan)
    root = Parser(spec_data).toTree([22])
    #print root._str_tree(indent=2, attrs=True, recursive=True)
    print root.tree


REPORTING_QUIET    = 'quiet'
REPORTING_STANDARD = 'standard'
REPORTING_VERBOSE  = 'verbose'
SCAN_LIST_ALL      = 'all'


def get_user_parameters():
    '''configure user's command line parameters from sys.argv'''
    global hdf5_extension
    import argparse
    parser = argparse.ArgumentParser(prog='spec2nexus', 
                                     description=main.__doc__.strip())
    parser.add_argument('infile', 
                        action='store', 
                        nargs='+', 
                        help="SPEC data file name(s)")
    msg =  "NeXus HDF5 output file extension"
    msg += ", default = %s" % hdf5_extension
    parser.add_argument('-e', 
                        '--hdf5-extension',
                        action='store', 
                        dest='hdf5_extension', 
                        help=msg, 
                        default=hdf5_extension)
    parser.add_argument('-f', 
                        '--force-overwrite', 
                        action='store_true',
                        dest='force_write',
                        help='overwrite output file if it exists',
                        default=False)
    parser.add_argument('-V', 
                        '--version', 
                        action='version', 
                        version=spec2nexus.__version__)
    msg =  'specify which scans to save'
    msg += ', such as: -s all  or  -s 1  or  -s 1,2,3-5  (no spaces!)'
    msg += ', default = %s' % SCAN_LIST_ALL
    parser.add_argument('-s', 
                        '--scan',
                        nargs=1, 
                        #action='append',
                        dest='scan_list',
                        default=SCAN_LIST_ALL,
                        help=msg)
    parser.add_argument('-t', 
                        '--tree-only', 
                        action='store_true',
                        dest='tree_only',
                        help='print NeXus/HDF5 node tree (does not save to a file)',
                        default=False)

    group = parser.add_mutually_exclusive_group()
    group.set_defaults(reporting_level=REPORTING_STANDARD)
    msg =  'suppress all program output (except errors)'
    msg += ', do not use with -v option'
    group.add_argument('-q', 
                       '--quiet', 
                       dest='reporting_level',
                       action='store_const',
                       const=REPORTING_QUIET,
                       help=msg)
    msg =  'print more program output'
    msg += ', do not use with -q option'
    group.add_argument('-v', 
                       '--verbose', 
                       dest='reporting_level',
                       action='store_const',
                       const=REPORTING_VERBOSE,
                       help=msg)

    return parser.parse_args()


def parse_scan_list_spec(scan_list_spec):
    '''parses the argument of the -s option, returns a scan number list'''
    # can this be simpler?
    sl = scan_list_spec[0].split(',')   # FIXME: why is this a list?

    scan_list = []
    for item in sl:
        sublist = item.split('-')
        if len(sublist) == 1:
            scan_list.append(int(sublist[0]))
        elif len(sublist) == 2:
            scan_list += range(int(sublist[0]), int(sublist[1])+1)
        else:
            raise ValueError, 'improper scan list specifier: ' + sublist

    sl = []
    for item in sorted(scan_list):
        if item not in sl:
            sl.append(item)

    return sl


def pick_scans(all_scans, opt_scan_list):
    '''
    edit opt_scan_list for the scans to be converted
    
    To be converted, a scan number must be first specified in opt_scan_list
    and then all_scans is checked to make sure that scan exists.
    The final list is returned.
    '''
    if opt_scan_list == SCAN_LIST_ALL:
        scan_list = all_scans
    else:
        scan_list = opt_scan_list
        for item in scan_list:
            if item not in all_scans:
                scan_list.remove(item)
    return scan_list


def main():
    '''spec2nexus: Convert SPEC data file into a NeXus HDF5 file.'''
    
    # developer test items
    #sys.argv.append('--help')
    #sys.argv.append('-V')
    #sys.argv.append('-q')
    #sys.argv.append('-v')
    #sys.argv.append('-f')
    #sys.argv.append('-t')
    #sys.argv.append('-s 19,1-4,19')
    #sys.argv.append('-s 2')
    #sys.argv.append(os.path.join('data', 'APS_spec_data.dat'))
    #sys.argv.append(os.path.join('data', '33id_spec.dat'))
    #sys.argv.append(os.path.join('data', '33bm_spec.dat'))

    user_parms = get_user_parameters()

    spec_data_file_name_list = user_parms.infile

    if user_parms.scan_list != SCAN_LIST_ALL:
        user_parms.scan_list = parse_scan_list_spec(user_parms.scan_list)
    
    if user_parms.tree_only:
        if user_parms.reporting_level in (REPORTING_QUIET):
            msg = 'do not use -t/--tree-only and -q/--quiet options together'
            raise ValueError, msg
        elif user_parms.reporting_level in (REPORTING_VERBOSE):
            user_parms.reporting_level = REPORTING_STANDARD
    else:
        if not user_parms.hdf5_extension.startswith(os.extsep):
            user_parms.hdf5_extension = os.extsep + user_parms.hdf5_extension

    for spec_data_file_name in spec_data_file_name_list:
        if not os.path.exists(spec_data_file_name):
            msg = 'File not found: ' + spec_data_file_name
            print msg
        else:
            if user_parms.reporting_level in (REPORTING_STANDARD, REPORTING_VERBOSE):
                if not user_parms.tree_only:
                    print 'reading SPEC data file: '+spec_data_file_name
            spec_data = prjPySpec.SpecDataFile(spec_data_file_name)
        
            scan_list = pick_scans(spec_data.scans.keys(), user_parms.scan_list)
            if user_parms.reporting_level in (REPORTING_VERBOSE):
                print '  discovered', len(spec_data.scans.keys()), ' scans'
                print '  converting scans: '  +  ', '.join(map(str, scan_list))

            tree = Parser(spec_data).toTree(scan_list)
        
            if user_parms.tree_only:
                print tree.tree
            else:
                basename = os.path.splitext(spec_data_file_name)[0]
                nexus_output_file_name = basename + user_parms.hdf5_extension
                if user_parms.force_write or not os.path.exists(nexus_output_file_name):
                    tree.save(nexus_output_file_name)
                    if user_parms.reporting_level in (REPORTING_STANDARD, REPORTING_VERBOSE):
                        print 'wrote NeXus HDF5 file: ' + nexus_output_file_name


if __name__ == "__main__":
    #developer_test()
    main()
