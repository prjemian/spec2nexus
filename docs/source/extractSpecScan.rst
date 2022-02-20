.. _extractSpecScan:

extractSpecScan
###############

Command line tool to extract scan data from a SPEC data file.

.. index:: examples; extractSpecScan


How to use **extractSpecScan**
******************************

Extract one scan from a SPEC data file::

    user@host ~$ extractSpecScan data/APS_spec_data.dat -s 1 -c mr USAXS_PD I0 seconds

the usage message::

   user@host ~$ extractSpecScan
   usage: extractSpecScan [-h] [-v] [--nolabels] -s SCAN [SCAN ...] -c COLUMN
                          [COLUMN ...] [-G] [-P] [-Q] [-V] [--quiet | --verbose]
                          spec_file

the version number::

   user@host ~$ extractSpecScan -v
   2017.0201.0

the help message::

   user@host ~$ extractSpecScan -h
   usage: extractSpecScan [-h] [-v] [--nolabels] -s SCAN [SCAN ...] -c COLUMN
                          [COLUMN ...] [-G] [-P] [-Q] [-V] [--quiet | --verbose]
                          spec_file
   
   Save columns from SPEC data file scan(s) to TSV files URL:
   https://prjemian.github.io/spec2nexus//extractSpecScan.html v2016.1025.0
   
   positional arguments:
     spec_file             SPEC data file name(s)
   
   optional arguments:
     -h, --help            show this help message and exit
     -v, --version         print version number and exit
     --nolabels            do not write column labels to output file (default:
                           write labels)
     -s SCAN [SCAN ...], --scan SCAN [SCAN ...]
                           scan number(s) to be extracted (must specify at least
                           one)
     -c COLUMN [COLUMN ...], --column COLUMN [COLUMN ...]
                           column label(s) to be extracted (must specify at least
                           one)
     -G                    report scan Geometry (#G) header information
     -P                    report scan Positioners (#O & #P) header information
     -Q                    report scan Q (#Q) header information
     -V                    report scan (UNICAT-style #H & #V) header information
     --quiet               suppress all program output (except errors), do not
                           use with --verbose option
     --verbose             print more program output, do not use with --quiet
                           option

Example
*******

Extract four columns (mr, USAXS_PD, I0, seconds) from two
scans (1, 6) in a SPEC data file::

   $ extractSpecScan data/APS_spec_data.dat -s 1 6 -c mr USAXS_PD I0 seconds

   program: /path/to/extractSpecScan.py
   read: data/APS_spec_data.dat
   wrote: data/APS_spec_data_1.dat
   wrote: data/APS_spec_data_6.dat

Here's the contents of *data/APS_spec_data_6.dat*::

   # mr  USAXS_PD I0 seconds
   15.61017 9.0   243.0 0.3
   15.61 13.0  325.0 0.3
   15.60984 19.0  460.0 0.3
   15.60967 30.0  609.0 0.3
   15.6095  54.0  883.0 0.3
   15.60934 161.0 1780.0   0.3
   15.60917 499.0 3649.0   0.3
   15.609   1257.0   6588.0   0.3
   15.60884 2832.0   10245.0  0.3
   15.60867 7294.0   13118.0  0.3
   15.6085  139191.0 16527.0  0.3
   15.60834 299989.0 17893.0  0.3
   15.60817 299989.0 18276.0  0.3
   15.608   299989.0 18240.0  0.3
   15.60784 299989.0 18266.0  0.3
   15.60767 299989.0 18616.0  0.3
   15.6075  299989.0 19033.0  0.3
   15.60734 299989.0 19036.0  0.3
   15.60717 299988.0 18587.0  0.3
   15.607   299989.0 17471.0  0.3
   15.60684 123003.0 14814.0  0.3
   15.60667 11060.0  11861.0  0.3
   15.6065  2217.0   8131.0   0.3
   15.60634 637.0 4269.0   0.3
   15.60617 254.0 2632.0   0.3
   15.606   132.0 1927.0   0.3
   15.60584 79.0  1406.0   0.3
   15.60567 58.0  1075.0   0.3
   15.6055  32.0  695.0 0.3
   15.60534 17.0  374.0 0.3
   15.60517 10.0  245.0 0.3

source code documentation
*************************

.. automodule:: spec2nexus.extractSpecScan
    :members: 
    :synopsis: Save columns from SPEC data file scan(s) to TSV files
 
