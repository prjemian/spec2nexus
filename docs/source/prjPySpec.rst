.. _prjPySpec:

:mod:`spec2nexus.prjPySpec`
###########################

Library of classes to read the contents of a SPEC data file.

.. index:: examples; prjPySpec

How to use :mod:`spec2nexus.prjPySpec`
**************************************

:mod:`spec2nexus.prjPySpec` provides Python support to read 
the scans in a SPEC data file.  (It does not provide a command-line interface.)
Here is a quick example how to use :mod:`~spec2nexus.prjPySpec`:

.. code-block:: guess
   :linenos:
   
   from spec2nexus.prjPySpec import SpecDataFile
   
   specfile = SpecDataFile('data/33id_spec.dat')
   print 'SPEC file name:', specfile.specFile
   print 'SPEC file time:', specfile.headers[0].date
   print 'number of scans:', len(specfile.scans)
   
   for scanNum, scan in specfile.scans.items():
       print scanNum, scan.scanCmd

For one example data file provided with :mod:`spec2nexus.prjPySpec`, the output starts with:

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

----

.. index:: SPEC data file keys

.. _spec.keys:

SPEC data files
***************

The SPEC data file format is described in the SPEC manual. [#]_
This manual is taken as a suggested starting point for most users.
Data files with deviations from this standard are produced at some facilities.


.. [#] SPEC manual: http://www.certif.com/spec_manual/user_1_4_1.html

..
   :see: http://www.certif.com/cplot_manual/ch0c_C_11_3.html
   
   The scan files contain control lines, data lines and blank lines. 
   
   * *Control lines* contain a # character in the first column followed by a command word. 
   * *Data lines* generally contain a row of numbers. 
   * *Special data lines* containing MCA data begin with an @ character followed by a row of numbers.

   The control conventions used by scans.4 are as follows:
   
   #S N
       starts a new scan. Here, N is the user's numbering scheme and is the number 
       used when retrieving by scan number (+S). Most often the scan number is the 
       position of the scan in the file.
   
   #M N
       indicates data was taken counting to N monitor counts.
   
   #T N
       indicates data was taken counting for N seconds.
   
   #N N [M]
       indicates there are N columns of data. If M is present, it indicates there 
       are M sets of data columns on each line. When collecting data from a 
       multi-channel analyzer, for example, the data might be arranged with 
       16 points per line in the file to make the file easier to scan by eye. 
       In such a case, the control line would be #N 1 16.
   
   #I N
       is for an optional multiplicative intensity-normalization factor.
   
   #@MCA
       indicates the scan contains MCA data. If the +M option is selected, 
       x (2D or 3D) or y (3D only) values will be calculated automatically. 
       In three-column mode, whether it is x or y depends on whether the x=M or
       y=M command line option is selected or on which interactive response was 
       given. Data in the lines starting with @A will be stuffed into the 
       y (2D) or z (3D) data array.
   
   #@CALIB a b c
       gives calibration factors for MCA data. The x (2D or 3D) or y (3D only) 
       values will be calculated using the formula::
   
         xi = a + b*i + c*i*i
   
       where i is the point number, starting from zero. Calibration factors can 
       be changed within the data portion of a scan for subsequent MCA data by the line
   
         @CALIB a b c
   
       Before each scan is read by scans.4, the calibration parameters are 
       initialized to zero.
   
    The following control lines are not commands but are printed out as 
    they are encountered while reading a scan:
   
   #C
       is a comment line.
   
   #D
       is followed by the date and time the scan was taken.
   
   #L label1 label2 ...
       is the data-column labels, with each label separated from the next by two spaces.
   
       For example, a very simple file might have::
   
          #S 1
          #N 3
          #L Temperature  Voltage  Counts
          23.4 1.01 30456
          23.6 1.015 24000
      
          #S 2 etc.





.. index:: SPEC; data file structure
.. index:: SPEC; control lines
.. index:: SPEC; data lines
.. index:: SPEC; special data lines

Assumptions about data file structure
=====================================

These assumptions are used to parse SPEC data files:

#. SPEC data files are text files organized by lines.
   The lines can be categorized as: **control lines**, **data lines**, and blank lines. 
   
   ==============   =========================================================================
   line type        description
   ==============   =========================================================================
   *control*        contain a # character in the first column followed by a command word [#]_
   *data*           generally contain a row of numbers (the scan data)
   *special data*   containing MCA data [#]_
   ==============   =========================================================================

#. Lines in a SPEC data file are grouped into a file header block or a scan block.
   A block consists of a series of control, data, and blank lines.
   
   SPEC data files are composed of a sequence of a single file header block 
   and zero or more scan blocks. [#]_

#. A file header block begins with these control lines in order: #F #E #D #C, such as::

    #F samplecheck_7_17_03
    #E 1058427452
    #D Thu Jul 17 02:37:32 2003
    #C psic  User = epix

#. A scan block begins with these command lines in order: #S #D, such as::

    #S 78  ascan  del 84.6484 84.8484  20 1
    #D Thu Jul 17 08:03:54 2003
   
..	[#] See :ref:`control_line_examples`

.. [#] See :ref:`mca_data_example`

.. [#]  It is very unusual to have more than one file header block in a SPEC data file.


.. _control_line_list:

Control lines (keys) defined by SPEC
====================================

Here is a list of keys (command words) from the comments in the *file.mac* (SPEC v6) macro source file:

===============  ===================================================================================
command word     description
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
#@MCA fmt        this scan contains MCA data (array_dump() format, as in ``"%16C"``)
#@CALIB a b c    coefficients for ``x[i] = a + b * i + c * i * i`` for MCA data
#@CHANN n f l r  MCA channel information (number_saved, first_saved, last_saved, reduction coef)
#@CTIME p l r    MCA count times (preset_time, elapsed_live_time, elapsed_real_time)
#@ROI n f l      MCA ROI channel information (ROI_name, first_chan, last_chan)
===============  ===================================================================================

.. index:: examples; SPEC control lines

.. _control_line_examples:

Example of Control Lines
++++++++++++++++++++++++

The command word of a control line may have a number at the end, 
indicating it is part of a sequence, such as these control lines 
(see :ref:`control_line_list` for how to interpret):

.. code-block:: guess
   :linenos:
   
   #D Wed Nov 03 13:42:03 2010
   #T 0.3  (seconds)
   #G0 0
   #G1 0
   #G3 0
   #G4 0
   #Q 
   #P0 -0.5396381 -0.5675 0.395862 0.7425 40.489861 0 5.894899e-07 11
   #P1 24 0 -1.19 9.0028278 25.000378 -22.29064 1.5 5
   #P2 -43 -0.01 98 11.8 0 -6.3275 111.52875 -8.67896
   #P3 -0.11352 1e-05 0.199978 0.4001875 1.2998435 15.6077 0 0
   #P4 3.03 0 3.21 6.805 2.835 2.4475 0.9355 -0.072
   #P5 1.31 0.0875 2442.673 -0.391 12 -14.4125 15.498553 

.. index:: examples; SPEC MCA data

.. _mca_data_example:

Example of MCA data lines
+++++++++++++++++++++++++

Lines with MCA array data begin with the **@A** command word.
(If such a data line ends with a continuation character ``\``, 
the next line is read as part of this line.)

This is an example of a 91-channel MCA data array with trivial (zero) values:

.. code-block:: guess
   :linenos:
   
   @A 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\
    0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\
    0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\
    0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\
    0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\
    0 0 0 0 0 0 0 0 0 0 0 


Supported header keys (command words)
=====================================

This is the table of SPEC data file keys recognized in file header blocks
and handled by :mod:`~spec2nexus.prjPySpec`:

====   ========================================================
key    description
====   ========================================================
#F     original data file name (starts a file header block)
#D     date/time stamp
#C     comment
#E     the UNIX epoch (seconds from 00:00 GMT 1/1/70)
#O     positioner names (numbered rows: #O0, #O1, ...)
#H     UNICAT metadata names (numbered rows: #H0, #H1, ...)
====   ========================================================


Supported scan keys (command words)
===================================

This is the table of SPEC data file keys recognized in scan blocks
and handled by :mod:`~spec2nexus.prjPySpec`:

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

source code summary
*******************

classes
=======

.. autosummary::
   :nosignatures:

   ~spec2nexus.prjPySpec.SpecDataFile
   ~spec2nexus.prjPySpec.SpecDataFileHeader
   ~spec2nexus.prjPySpec.SpecDataFileScan

methods
=======

.. autosummary::
   :nosignatures:

   ~spec2nexus.prjPySpec.strip_first_word

exceptions
==========

.. autosummary::
   :nosignatures:

   ~spec2nexus.prjPySpec.SpecDataFileNotFound
   ~spec2nexus.prjPySpec.SpecDataFileCouldNotOpen
   ~spec2nexus.prjPySpec.SpecDataFileNotFound



dependencies
============

.. autosummary::
   :nosignatures:
   
   os
   re
   sys

documentation
=============

.. automodule:: spec2nexus.prjPySpec
    :members: 
    :synopsis: Classes to read the contents of a SPEC data file.
 
