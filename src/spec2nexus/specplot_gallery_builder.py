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
crawl directories for SPEC data files and build default plots for all scans

This script could be called from *cron*, such as:

    # every five minutes (generates no output from outer script)
    0-59/5 * * * *  /some/directory/specplot_gallery_builder.py

tips if too many processes have been started::

    kill -9 `psg bash | awk '/specplot_shell_script.sh/ {print $2}' -`
    kill -9 `psg python | awk '/specplot_gallery.py/ {print $2}' -`

'''

# TODO: do not start this script if it is running from previous call

import argparse
import os
import sys
from spec2nexus import specplot_gallery, spec

LOGFILE_NAME = 'specplot_files.log'

"""



#--------------------------------------------------------------------
#
# change the SPEC_DATA_PATTERN periodically to reduce the search time
# this is very important, for example, just this one directory:
#   /data/USAXS_data/2013-1*/*.dat  takes about a minute to run
#
#SPEC_DATA_PATTERN=/data/USAXS_data/2010-04/*.dat
#SPEC_DATA_PATTERN=/data/USAXS_data/201*-*/*.dat
#SPEC_DATA_PATTERN=/data/USAXS_data/2013-1*/*.dat
#SPEC_DATA_PATTERN=/data/USAXS_data/2014-*/*.dat
#SPEC_DATA_PATTERN=/share1/USAXS_data/2015-*/*.dat

SPEC_DATA_PATTERN=/share1/USAXS_data/2016-*/*.dat

FILE_LIST=`/bin/ls -1 $SPEC_DATA_PATTERN`

#--------------------------------------------------------------------

cd $SHELL_DIR
echo "#= $$ --Start--- `/bin/date`" >> $LOGFILE 2>&1
$PROGRAM $FILE_LIST >> $LOGFILE 2>&1
echo "#= $$ --Done---------------------------------- `/bin/date`" >> $LOGFILE 2>&1
"""

def main():
    doc = __doc__.strip().splitlines()[0]
    p = argparse.ArgumentParser(description=doc)
    
    p.add_argument(
        'specDirs',  
        nargs='+',  
        help="directory name(s) with SPEC data file(s)")
    
    p.add_argument(
        '-r', 
        action='store_true', 
        default=False,
        dest='reverse_chronological',
        help='sort images in reverse chronolgical order')

    pwd = os.getcwd()
    msg = 'base directory for output'
    msg += ' (default:' + pwd + ')'
    p.add_argument('-d', '--dir', help=msg)

    args = p.parse_args()
    
    specplots_dir = args.dir or pwd
    file_list = []
    for path in args.specDirs:
        for item in os.listdir(path):
            fname = os.path.join(path, item)
            if os.path.isfile(fname) and spec.is_spec_file(fname):
                file_list.append(fname)

    if len(file_list) == 0:
        return      # no work to do, return silently

    specplot_gallery.PlotSpecFileScans(
        file_list, 
        specplots_dir, 
        reverse_chronological=args.reverse_chronological)


if __name__ == '__main__':
    import logging
    import shutil
    import tempfile
    
    tempdir = tempfile.mkdtemp()
    sys.argv.append('-d')
    sys.argv.append(tempdir)
    sys.argv.append(os.path.join('data'))
    logging.disable(logging.CRITICAL)
    main()
    logging.shutdown()
    shutil.rmtree(tempdir)
    logging.disable(logging.NOTSET)
