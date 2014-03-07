.. _prjPySpec:

prjPySpec
#########

Library of classes to read the contents of a SPEC data file.

.. index:: examples

How to use :mod:`spec2nexus.prjPySpec`
**************************************

The file **prjPySpec.py** provides Python support to read 
the scans in a SPEC data file.  (It does not provide a command-line interface.)
Here is a quick example how to use **prjPySpec.py**:

.. code-block:: guess
    :linenos:

   	from spec2nexus.prjPySpec import SpecDataFile
   	
   	specfile = SpecDataFile('data/33id_spec.dat')
   	print 'SPEC file name:', specfile.specFile
   	print 'SPEC file time:', specfile.headers[0].date
   	print 'number of scans:', len(specfile.scans)
   	
   	for scanNum, scan in specfile.scans.items():
   	    print scanNum, scan.scanCmd

For one example data file provided with spec2nexus, the output starts with:

.. code-block:: guess
    :linenos:

   	SPEC file name: samplecheck_7_17_03
   	SPEC file time: Thu Jul 17 02:37:32 2003
   	number of scans: 106
   	1  ascan  eta 43.6355 44.0355  40 1
   	2  ascan  chi 73.47 73.87  40 1
   	3  ascan  del 84.6165 84.8165  20 1
   	4  ascan  del 84.5199 84.7199  20 1
   	5  ascan  del 84.3269 84.9269  30 1
   	...

How to read one scan
====================

Here is an example how to read one scan:

.. code-block:: guess
    :linenos:

      from spec2nexus.prjPySpec import SpecDataFile
      
      specfile = SpecDataFile('data/33id_spec.dat')
      specscan = specfile.getScan(5)
      print specscan.scanNum
      print specscan.scanCmd

which has this output::

   5
   ascan  del 84.3269 84.9269  30 1

The data columns are provided in a dictionary.  Using the example above,
the dictionary is ``specscan.data`` where the keys are the column labels (from the
#L line) and the values are from each row.  It is possible to make a default
plot of the last column vs. the first column.  Here's how to find that data:

.. code-block:: guess
    :linenos:

      x_label = specscan.L[0]          # first column from #L line
      y_label = specscan.L[-1]         # last column from #L line
      x_data = specscan.data[x_label]  # data for first column
      y_data = specscan.data[y_label]  # data for last column

Get a list of the scans
=======================

The complete list of scan numbers from the data file is obtained
(sorting is necessary since the list of dictionary keys is returned
in a scrambled order)::

  all_scans = sorted(specfile.scans.keys())

.. index:: SPEC data file keys

.. _spec.keys:

SPEC data file keys
*******************

SPEC data files are composed of a sequence of file header block and scan blocks.

..

	2014-03-07 from Gerry

	Here is a list from the comments in the new file.mac macro source file:
	
	===============  ===================================================================================
	key              description
	===============  ===================================================================================
	#C               comment line
	#D date          current date and time in UNIX format
	#E num           the UNIX epoch (seconds from 00:00 GMT 1/1/70)
	#F name          name by which file was created
	#G1 ...          geometry parameters from G[] array (geo mode, sector, etc)
	#G2 ...          geometry parameters from U[] array (lattice constants, orientation reflections)
	#G3 ...          geometry parameters from UB[] array (orientation matrix)
	#G4 ...          geometry parameters from Q[] array (lambda, frozen angles, cut points, etc)
	#I num           a normalizing factor to apply to the data
	#j% ...          mnemonics of counter (% = 0,1,2,... with eight counters per row)
	#J% ...          names of counters (each separated by two spaces)
	#L s1  ...       labels for the data columns
	#M num           data was counted to this many monitor counts
	#N num [num2]    number of columns of data [ num2 sets per row ]
	#o% ...          mnemonics of motors (% = 0,1,2,... with eight motors per row)
	#O% ...          names of motors (each separated by two spaces)
	#P% ...          positions of motors corresponding to above #O/#o
	#Q               a reciprocal space position (H K L)
	#R               user-defined results from a scan
	#S num           scan number
	#T num           data was counted for this many seconds
	#U               user defined
	#X               a temperature
	#@MCA fmt        this scan contains MCA data (array_dump() format, as in "%16C")
	#@CALIB a b c    coefficients for x[i] = a + b * i + c * i * i for MCA data
	#@CHANN n f l r  MCA channel information (number_saved, first_saved, last_saved, reduction coef)
	#@CTIME p l r    MCA count times (preset_time, elapsed_live_time, elapsed_real_time)
	#@ROI n f l      MCA ROI channel information (ROI_name, first_chan, last_chan)
	===============  ===================================================================================





Tables of keys in SPEC data file header blocks
==============================================

This is the table of SPEC data file keys recognized in file header blocks
and handled by this code:

====   ========================================================
key    description
====   ========================================================
#F     original data file name (starts a file header block)
#D     date/time stamp
#C     comment
#E     epoch (offset number of seconds since 1970)
#O     positioner names (numbered rows: #O0, #O1, ...)
#H     UNICAT metadata names (numbered rows: #H0, #H1, ...)
====   ========================================================


Tables of keys in SPEC data file scan blocks
============================================

This is the table of SPEC data file keys recognized in scan blocks
and handled by this code:

====   ===========================================================
key    description
====   ===========================================================
#S     scan (starts a scan block)
#C     comment
#D     date/time stamp
#G     diffractometer geometry (numbered rows: #G0, #G1, ...)
#L     data column labels
#M     counting against this constant monitor count (see #T)
#N     number of data columns
#P     positioner values at start of scan
#Q     hkl at start of scan (numbered rows: #P0, #P1, ...)
#V     UNICAT metadata values (numbered rows: #V0, #V1, ...)
#T     counting against this constant number of seconds (see #M)
====   ===========================================================


----

source code classes
*******************

.. autosummary::
   :nosignatures:

   ~spec2nexus.prjPySpec.SpecDataFile
   ~spec2nexus.prjPySpec.SpecDataFileHeader
   ~spec2nexus.prjPySpec.SpecDataFileScan

source code methods
*******************

.. autosummary::
   :nosignatures:

   ~spec2nexus.prjPySpec.specScanLine_stripKey

source code documentation
*************************

.. automodule:: spec2nexus.prjPySpec
    :members: 
    :synopsis: Classes to read the contents of a SPEC data file.
    