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
Pull out named columns from scan(s) in a SPEC data file and save to TSV files

**Usage**::

  extractSpecScan.py /tmp/CeCoIn5 5 HerixE Ana5 ICO-C
  extractSpecScan.py ./testdata/11_03_Vinod.dat   2 12   USAXS.m2rp Monitor  I0

**General usage**::

  extractSpecScan.py ./path/to/specFile  scanNumbers  columnLabels

where the path to the spec data file can be relative, absolute, 
or no directory part given at all,
the scan numbers are integers, separated by spaces and the columns 
labels are character strings (not valid integers), separated by spaces.

.. note:: TSV: tab-separated values

Compatible with Python 2.6+
'''


import prjPySpec
import os
import sys


PrintLabels = True      # put column labels in output file


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


def extractScans(cmdArgs):
    '''
    read the data file, find each scan, find the columns, save the data
    
    :param [str] cmdArgs: command line arguments split into a list, as in sys.argv
    
    .. note:: Each column label must match *exactly* the name of a label
       in each chosen SPEC scan number or the program will skip that particular scan
       
       If more than one column matches, the first match will be selected.
    
    example output::

        # USAXS.m2rp    Monitor    I0
        1.9475    65024    276
        1.9725    64845    352
        1.9975    65449    478
    
    '''
    global PrintLabels
    specFile, scanList, column_labels = parseCmdLine(cmdArgs)

    print "program: " + sys.argv[0]
    # now open the file and read it
    specData = prjPySpec.specDataFile(specFile)
    print "read: " + specFile
    
    for scanNum in scanList:
        outFile = makeOutputFileName(specFile, scanNum)
        # assume that this data file started with #S 1 (scan 1)
        scan = specData.scans[scanNum-1]
        # TODO: since this might not be true for some files, make this more robust.
        # Better to make an interface in prjPySpec and call that here:
        #   scan = specData.get_scan(scanNum)
    
        # get the column numbers corresponding to the column_labels
        column_numbers = []
        for label in column_labels:
            if label in scan.L:
                # report all columns in order specified on command-line
                column_numbers.append( scan.L.index(label) )
            else:
                msg = 'column label "' + label + '" not found in scan #'
                msg += str(scanNum) + ' ... skipping'
                print msg       # report all mismatched column labels
    
        if len(column_numbers) == len(column_labels):   # must be perfect matches
            txt = []
            if PrintLabels:
                txt.append( '# ' + '\t'.join(column_labels) )
            for data_row in scan.data_lines:
                data_row = data_row.split()
                row_data = [data_row[col] for col in column_numbers]
                txt.append( '\t'.join(row_data) )
            result = '\n'.join(txt)
        
            fp = open(outFile, 'w')
            fp.write(result)
            fp.close()
            print "wrote: " + outFile


def parseCmdLine(cmdArgs):
    '''
    interpret the command-line arguments (avoid getopts, optparse, and argparse)
    
    :param [str] cmdArgs: command line arguments split into a list, as in sys.argv
    
    :returns tuple: specFile, scanList, column_labels
    
    :param str specFile: name of existing SPEC data file to be read
    :param [int] scanList: list of chosen SPEC scan numbers
    :param [str] column_labels: list of column labels
    '''
    global PrintLabels

    if len(cmdArgs) < 4:
        print "usage: extractSpecScan.py specFile scanNum [scanNum [...]] [-nolabels] col1 [col2 [col3 [...]]]"
        exit(1)

    # positional argument
    specFile = cmdArgs[1]
    if not os.path.exists(specFile):
        raise RuntimeError, "file not found: " + specFile

    # variable length argument (optparse cannot handle, argparse requires python 2.7+)
    # read the list of scan numbers as integers
    # list ends when we get to a column label
    # column labels are not integers
    pos = 2
    scanList = []
    while True:
        try:
            scanNum = int(cmdArgs[pos])
            if scanNum not in scanList:
                # avoid reporting the same scan number more than once
                scanList.append( scanNum )
            pos += 1
        except ValueError:
            break

    # check for the '-nolabels' option to disable column labels in the output file
    if cmdArgs[pos] == '-nolabels':
        PrintLabels = False
        pos += 1
    
    # variable length argument
    # all that is left on the line are column labels
    column_labels = []
    for label in cmdArgs[pos:]:
        if label not in column_labels:
            # avoid reporting the same column label more than once
            column_labels.append( label )
    return specFile, scanList, column_labels


def main():
    extractScans(sys.argv)


def test():
    # test file for sector 30 is here:
    #  /home/beams/IXS/Data/HERIX/SPEC/2013-1/Weber/CeCoIn5
    # copy it and use the scratch copy (to be safe)
    # cp /home/beams/IXS/Data/HERIX/SPEC/2013-1/Weber/CeCoIn5 /tmp
    cmdLine = sys.argv[0] + r' /tmp/CeCoIn5   5 6 7 8 9   HerixE Ana5 ICO-C'

    # alternate test data from USAXS archive
    cmdLine = sys.argv[0] + r' ./testdata/11_03_Vinod.dat   1 2 12   USAXS.m2rp Monitor  I0'
    
    extractScans(cmdLine.split())


if __name__ == "__main__":
    main()
    #test()
