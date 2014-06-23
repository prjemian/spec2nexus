#!/usr/bin/python

#-----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
#-----------------------------------------------------------------------------


'''
Save columns from SPEC data file scan(s) to TSV files

.. note:: TSV: tab-separated values

**Usage**::

  extractSpecScan.py /tmp/CeCoIn5 -s 5 -c HerixE Ana5 ICO-C
  extractSpecScan.py ./testdata/11_03_Vinod.dat   -s 2 12   -c USAXS.m2rp Monitor  I0

**General usage**::

    usage: extractSpecScan [-h] [--nolabels] [-s SCAN [SCAN ...]] [-c COLUMN [COLUMN ...]] spec_file

Save columns from SPEC data file scan(s) to TSV files


positional arguments:

========================  ==========================================================================
argument                  description
========================  ==========================================================================
spec_file                 SPEC data file name (path is optional, can use relative or absolute)
========================  ==========================================================================


optional arguments:

=============================  ==========================================================================
argument                       description
=============================  ==========================================================================
-h, --help                     show this help message and exit
--nolabels                     do not write column labels to output file (default: write labels)
-s SCAN [SCAN ...]             scan number(s) to be extracted, must be integers
--scan SCAN [SCAN ...]         same as *-s* option
-c COLUMN [COLUMN ...]         column label(s) to be extracted
--column COLUMN [COLUMN ...]   same as *-c* option
=============================  ==========================================================================

.. note:: column names MUST appear in all chosen scans

Compatible with Python 2.7+
'''


import os
import sys
import prjPySpec


#-------------------------------------------------------------------------------------------


def makeOutputFileName(specFile, scanNum):
    '''
    return an output file name based on specFile and scanNum
    
    :param str specFile: name of existing SPEC data file to be read
    :param int scanNum: number of chosen SPEC scan

    append scanNum to specFile to get output file name 
    (before file extension if present)
    
    Always add a file extension to the output file.
    If none is present, use ".dat".
    
    Examples:
    
    ===========  =======   ==============
    specFile     scanNum   outFile
    ===========  =======   ==============
    CeCoIn5      scan 5    CeCoIn5_5.dat
    CeCoIn5.dat  scan 77   CeCoIn5_77.dat
    ===========  =======   ==============
    '''
    name_parts = os.path.splitext(specFile)
    outFile = name_parts[0] + '_' + str(scanNum) + name_parts[1]
    return outFile


def get_user_parameters():
    '''configure user's command line parameters from sys.argv'''
    import argparse
    doc = __doc__.strip().splitlines()[0]
    parser = argparse.ArgumentParser(prog='extractSpecScan', description=doc)

    parser.add_argument('--nolabels', 
                        action='store_true',
                        help='do not write column labels to output file',
                        default=False)
    parser.add_argument('spec_file', 
                        action='store', 
                        nargs=1, 
                        help="SPEC data file name(s)")
    parser.add_argument('-s',
                        '--scan', 
                        action='store', 
                        nargs='+', 
                        type=int,
                        help="scan number(s) to be extracted")
    parser.add_argument('-c',
                        '--column', 
                        action='store', 
                        nargs='+', 
                        help="column label(s) to be extracted")

    args = parser.parse_args()

    if args.scan is None:
        raise KeyError, "must name at least one scan number to extract"
    if args.column is None:
        raise KeyError, "must name at least one column to extract"
    args.spec_file = args.spec_file[0]
    
    args.print_labels = not args.nolabels
    del args.nolabels

    return args


def main():
    '''
    read the data file, find each scan, find the columns, save the data
    
    :param [str] cmdArgs: Namespace from argparse, returned from get_user_parameters()
    
    ..  such as:
      Namespace(column=['x', 'y', 'I0', 'I'], print_labels=True, scan=[92, 95], spec_file=['data\\APS_spec_data.dat'])
    
    .. note:: Each column label must match *exactly* the name of a label
       in each chosen SPEC scan number or the program will skip that particular scan
       
       If more than one column matches, the first match will be selected.
    
    example output::

        # USAXS.m2rp    Monitor    I0
        1.9475    65024    276
        1.9725    64845    352
        1.9975    65449    478
    
    '''
    cmdArgs = get_user_parameters()

    print "program: " + sys.argv[0]
    # now open the file and read it
    specData = prjPySpec.SpecDataFile(cmdArgs.spec_file)
    print "read: " + cmdArgs.spec_file
    
    for scanNum in cmdArgs.scan:
        outFile = makeOutputFileName(cmdArgs.spec_file, scanNum)
        scan = specData.getScan(scanNum)
    
        # get the column numbers corresponding to the column_labels
        column_numbers = []
        for label in cmdArgs.column:
            if label in scan.L:
                # report all columns in order specified on command-line
                column_numbers.append( scan.L.index(label) )
            else:
                msg = 'column label "' + label + '" not found in scan #'
                msg += str(scanNum) + ' ... skipping'
                print msg       # report all mismatched column labels
    
        if len(column_numbers) == len(cmdArgs.column):   # must be perfect matches
            txt = []
            if cmdArgs.print_labels:
                txt.append( '# ' + '\t'.join(cmdArgs.column) )
            data = [scan.data[item] for item in cmdArgs.column]
            for data_row in zip(*data):
                txt.append( '\t'.join(map(str, data_row)) )
        
            fp = open(outFile, 'w')
            fp.write('\n'.join(txt))
            fp.close()
            print "wrote: " + outFile


if __name__ == "__main__":
    main()
