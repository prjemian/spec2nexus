.. _spec:

:mod:`spec2nexus.spec`
######################

Library of classes to read the contents of a SPEC data file.

.. index:: examples; spec

How to use :mod:`spec2nexus.spec`
*********************************

:mod:`spec2nexus.spec` provides Python support to read
the scans in a SPEC data file.  (It does not provide a command-line interface.)
Here is a quick example how to use :mod:`~spec2nexus.spec`:

.. code-block:: guess
   :linenos:

   from spec2nexus.spec import SpecDataFile

   specfile = SpecDataFile('data/33id_spec.dat')
   print 'SPEC file name:', specfile.specFile
   print 'SPEC file time:', specfile.headers[0].date
   print 'number of scans:', len(specfile.scans)

   for scanNum, scan in specfile.scans.items():
       print scanNum, scan.scanCmd

For one example data file provided with :mod:`spec2nexus.spec`, the output starts with:

.. code-block::
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

   from spec2nexus.spec import SpecDataFile

   specfile = SpecDataFile('data/33id_spec.dat')
   specscan = specfile.getScan(5)
   print specscan.scanNum
   print specscan.scanCmd

which has this output::

   5
   ascan  del 84.3269 84.9269  30 1

Alternatively, it is possible to use choose a scan using `[scan_number]` syntax.
This code is equivalent to the above:

.. code-block:: guess

   from spec2nexus.spec import SpecDataFile

   specfile = SpecDataFile('data/33id_spec.dat')
   specscan = specfile[5]
   print specscan.scanNum
   print specscan.scanCmd

The data columns are provided in a dictionary.  Using the example above,
the dictionary is ``specscan.data`` where the keys are the column labels (from the
#L line) and the values are from each row.  It is possible to make a default
plot of the last column vs. the first column.  Here's how to find that data:

.. code-block:: python
   :linenos:

   x_label = specscan.L[0]          # first column from #L line
   y_label = specscan.L[-1]         # last column from #L line
   x_data = specscan.data[x_label]  # data for first column
   y_data = specscan.data[y_label]  # data for last column

Get a list of the scans
=======================

The complete list of scan numbers from the data file is obtained, sorted
alphabetically by scan number::

  all_scans = specfile.getScanNumbers()


Same list sorted by date & time::

  all_scans = specfile.getScanNumbersChronological()

.. index:: !slicing

Select from the list of the scans
=================================

.. sidebar: Slicing feature added in release 2021.2.0

Get a scan (or list of scans) by *slicing* from the
:class:`~spec2nexus.spec.SpecDataFile()` object.

EXAMPLES:

First, read a SPEC data file::

   >>> from spec2nexus.spec import SpecDataFile
   >>> specfile = SpecDataFile('data/CdOsO')

Show scan number 5::

   >>> specscan = specfile[5]
   >>> print(specscan)
   5  ascan  stblx 1.925 3.925  50 1

Show the last scan::

   >>> print(specfile[-1])
   73  ascan  micro_y 6.7515 7.1515  20 1

Show scan numbers below 4.  Since the slice uses ``:`` characters, it returns a
list of scans::

   >>> for specscan in specfile[:4]:
   ...    print(specscan)
   1  ascan  herixE -17.3368 -7.33676  40 1
   1  ascan  herixE -1.00571 18.9943  20 30
   2  ascan  herixE -22.3505 -12.3505  40 1
   3  ascan  micro_y 4.75 6.75  50 1

Note there are two scans with scan number ``1``.  Slice the first scan number 1::

   >>> for specscan in specfile[1:2:0]:
   ...    print(specscan)
   1  ascan  herixE -17.3368 -7.33676  40 1

Slice the second scan number 1::

   >>> for specscan in specfile[1:2:1]:
   ...    print(specscan)
   1  ascan  herixE -1.00571 18.9943  20 30

Slice the last one scan number (same result)::

   >>> for specscan in specfile[1:2:-1]:  # slice the last one (same result)
   ...    print(specscan)
   1  ascan  herixE -1.00571 18.9943  20 30

Compare slicing methods.  Same scan::

   >>> specfile.getScan(1.1) == specfile[1.1]
   True

These are different scans::

   >>> specfile.getScan(1.1) == specfile[1]
   False

Note that ``getScan()`` returns a single scan while slicing (using `:`) returns a
list.  This fails::

   >>> specfile.getScan(1.1) == specfile[1:2:-1]
   False

and this succeeds::

   >>> [specfile.getScan(1.1)] == specfile[1:2:-1]
   True

.. index:: ! slice parameters
.. _slice_parameters:

Slice Parameters
++++++++++++++++

When slicing the data file object for scans (``specfile[given]``), consider that
the ``given`` slice has the parameters in the following table:

======================= =======================
slice                   meaning
======================= =======================
``i``                   one scan referenced by ``i`` (or ``None`` if not found)
``start:``              scan list from ``start`` (start <= scan_number)
``:finish``             scan list up to ``stop`` (scan_number < stop)
``::which``             scan list selecting from identical ``#S`` scan_number
``start:finish:which``  scan list with full slicing syntax
empty                   raises ``SyntaxError`` if ``[]``
``None``                raises ``TypeError`` if ``[None]``
``start:finish``        raises ``IndexError`` if ``start`` and ``finish`` have opposite signs (can't mix relative and absolute slicing)
======================= =======================

* ``start`` & ``finish`` take these meanings:
    * ``None`` : match all
    * string : will be converted to integer
    * ``>=0`` : match by scan number (from SPEC data file ``#S`` lines)
    * ``<0`` : match by relative position in the list of scans from :meth:`~spec2nexus.spec.SpecDataFile.getScanNumbersChronological()`

* `which` takes these meanings:
    * ``None`` : match all
    * string : will be converted to integer
    * ``<0`` : match by relative position in the list of duplicated scan numbers
    * ``>=0`` : match by specific number in the list of duplicated scan numbers

    Example: ``which=1`` will only match scan numbers with ``.1``
    while ``which=-1`` will match the last of every scan number.

**Many duplicated scan numbers**

When there are *many* duplicates of a scan number, it may be necessary to
use a string representation to distinguish between, for example ``.1`` (second
occurrence) and ``.10`` (eleventh occurrence).

Examples::

    >>> specfile['4.10'] != specfile[4.10]
    False
    >>> specfile['4.1'] == specfile[4.10]
    True

----

.. index:: SPEC data file keys

.. _spec.keys:

SPEC data files
***************

The SPEC data file format is described in the SPEC manual. [#]_
This manual is taken as a suggested starting point for most users.
Data files with deviations from this standard are produced at some facilities.


.. [#] SPEC manual: https://www.certif.com/spec_manual/user_1_4_1.html

..
   :see: https://www.certif.com/cplot_manual/ch0c_C_11_3.html

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

#. Lines in a SPEC data file start with a file name control line,
   then series of blocks.  Each block may be either a file header block
   or a scan block.  (Most SPEC files have only one header block.  A new header
   block is created if the list of positioners is changed in SPEC
   without creating a new file.  SPEC users are encouraged to *always* start a new
   data file after changing the list of positioners.)
   A block consists of a series of control, data, and blank lines.

   SPEC data files are composed of a sequence of a single file header block
   and zero or more scan blocks. [#]_

#. A SPEC data file always begins with this control lines: #F, such as::

    #F samplecheck_7_17_03

#. A file header block begins with these control lines in order: #E #D #C, such as::

    #E 1058427452
    #D Thu Jul 17 02:37:32 2003
    #C psic  User = epix

#. A scan block begins with these command lines in order: #S #D, such as::

    #S 78  ascan  del 84.6484 84.8484  20 1
    #D Thu Jul 17 08:03:54 2003

..	[#] See :ref:`control_line_examples`

.. [#] See :ref:`mca_data_example`

.. [#]  It is very unusual to have more than one file header block in a SPEC data file.


.. _plugin_list:

Control lines (keys) defined by SPEC
====================================

Here is a list [#]_ of keys (command words) from the comments in the *file.mac* (SPEC v6) macro source file:

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

.. [#] Compare with :ref:`supplied_plugins`

.. index:: examples; SPEC control lines

.. _control_line_examples:

Example of Control Lines
++++++++++++++++++++++++

The command word of a control line may have a number at the end,
indicating it is part of a sequence, such as these control lines
(see :ref:`plugin_list` for how to interpret):

.. code-block::
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

.. code-block:: text
   :linenos:

   @A 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\
    0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\
    0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\
    0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\
    0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\
    0 0 0 0 0 0 0 0 0 0 0

Several MCA spectra may be written to a scan.  In this case, a number
follows **@A** indicating which spectrum, such as in this example with
four spectra:

.. code-block:: text
   :linenos:

	@A1 0 0 0 0 0 0 35 0 0 35
	@A2 0 0 0 0 0 0 0 35 0 35
	@A3 0 0 35 35 0 0 0 0 0 0
	@A4 0 0 0 0 0 35 35 0 35 0


Supported header keys (command words)
=====================================

The SPEC data file keys recognized by :mod:`~spec2nexus.spec`
are listed in :ref:`supplied_plugins`.


----

source code summary
*******************

classes
=======

.. autosummary::
   :nosignatures:

   ~spec2nexus.spec.SpecDataFile
   ~spec2nexus.spec.SpecDataFileHeader
   ~spec2nexus.spec.SpecDataFileScan

methods
=======

.. autosummary::
   :nosignatures:

   ~spec2nexus.utils.strip_first_word
   ~spec2nexus.spec.is_spec_file

exceptions
==========

.. autosummary::
   :nosignatures:

   ~spec2nexus.spec.SpecDataFileNotFound
   ~spec2nexus.spec.SpecDataFileCouldNotOpen
   ~spec2nexus.spec.SpecDataFileNotFound
   ~spec2nexus.spec.DuplicateSpecScanNumber
   ~spec2nexus.spec.UnknownSpecFilePart

dependencies
============

.. autosummary::
   :nosignatures:

   os
   re
   sys

.. _spec_scan_internal_structure:

internal structure of :class:`spec2nexus.spec.SpecDataFileScan`
===============================================================

The internal variables of a Python class are called *attributes*.
It may be convenient, for some, to think of them as *variables*.

scan attributes
+++++++++++++++

:parent:   *obj* - instance of :class:`spec2nexus.spec.SpecDataFile`
:scanNum:  *int* - SPEC scan number
:scanCmd:  *str* - SPEC command line
:raw:      *str* - text of scan, as reported in SPEC data file

scan attributes (variables) set after call to plugins
+++++++++++++++++++++++++++++++++++++++++++++++++++++

These attributes are only set *after* the scan's :meth:`interpret` method is called.
This method is called automatically when trying to read any of the following scan attributes:

:comments:     *[str]* - list of all comments reported in this scan
:data:         *{label,[number]}* - written by :meth:`spec2nexus.plugins.spec_common_spec2nexus.data_lines_postprocessing`
:data_lines:   *[str]* - raw data (and possibly MCA) lines with comment lines removed
:date:    	   *str* - written by :class:`spec2nexus.plugins.spec_common_spec2nexus.SPEC_Date`
:G:            *{key,[number]}* - written by :class:`spec2nexus.plugins.spec_common_spec2nexus.SPEC_Geometry`
:I:    	      *float* - written by :class:`spec2nexus.plugins.spec_common_spec2nexus.SPEC_NormalizingFactor`
:header:  	   *obj* - instance of :class:`spec2nexus.spec.SpecDataFileHeader`
:L:    	      *[str]* - written by :class:`spec2nexus.plugins.spec_common_spec2nexus.SPEC_Labels`
:M: 		      *str* - written by :class:`spec2nexus.plugins.spec_common_spec2nexus.SPEC_Monitor`
:positioner:   *{key,number}* - written by :class:`spec2nexus.plugins.spec_common_spec2nexus.SPEC_Positioners.postprocess`
:N:    	      *[int]* - written by :class:`spec2nexus.plugins.spec_common_spec2nexus.SPEC_NumColumns`
:P:    	      *[str]* - written by :class:`spec2nexus.plugins.spec_common_spec2nexus.SPEC_Positioners`
:Q:    	      *[number]* - written by :class:`spec2nexus.plugins.spec_common_spec2nexus.SPEC_HKL`
:S: 		      *str* - written by :class:`spec2nexus.plugins.spec_common_spec2nexus.SPEC_Scan`
:T: 		      *str* - written by :class:`spec2nexus.plugins.spec_common_spec2nexus.SPEC_CountTime`
:V:            *{key,number|str}* - written by :class:`spec2nexus.plugins.unicat_spec2nexus.UNICAT_MetadataValues`
:column_first: *str* - label of first (ordinate) data column
:column_last:  *str* - label of last (abscissa) data column

internal use only - do not modify
+++++++++++++++++++++++++++++++++

These scan attributes are for internal use only and are not part of the public interface.
Do not modify them or write code that depends on them.

:postprocessors:     *{key,obj}* - dictionary of postprocessing methods
:h5writers:          *{key,obj}* - dictionary of methods that write HDF5 structure
:__lazy_interpret__:  *bool* - Is *lazy* (on-demand) call to :meth:`interpret` needed?
:__interpreted__:     *bool* - Has :meth:`interpret` been called?


source code documentation
=========================

.. automodule:: spec2nexus.spec
    :members:
    :synopsis: Classes to read the contents of a SPEC data file.
