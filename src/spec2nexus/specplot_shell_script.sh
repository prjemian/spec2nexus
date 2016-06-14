#!/bin/bash

# TODO: might be useful to make this Python code (could run on any Python platform then)

# crawl directories for SPEC data files and build default plots for all scans

#--------------------------------------------------------------------
# This script could be called from cron such as
#
#   # every five minutes (generates no output from outer script)
#   0-59/5 * * * *  /some/directory/specplot_shell_script.sh
#--------------------------------------------------------------------

# TODO: do not start this script if it is running from previous call

#--------------------------------------------------------------------
# tips if too many processes have been started:
# kill -9 `psg bash | awk '/specplot_shell_script.sh/ {print $2}' -`
# kill -9 `psg python | awk '/specplot_gallery.py/ {print $2}' -`
#--------------------------------------------------------------------

SHELL_DIR=/some/directory
LOGFILE=$SHELL_DIR/specplot_files.log
PROGRAM=/APSshare/anaconda/x86_64/bin/specplot_gallery

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
