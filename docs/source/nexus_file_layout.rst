NeXus File Layout
#################

.. https://github.com/prjemian/spec2nexus/issues/192

    from spec2nexus import spec, writer
    sdf = spec.SpecDataFile("one-scan.dat")
    scans = sdf.getScanNumbersChronological()
    writer.Writer(sdf).save("one-scan.hdf5", scan_list=scans)
    !punx tree one-scan.hdf5

.. TODO:

    - NXdata documentation about how scan data is to be stored
    - documentation for counter_cross_reference
    - documentation for positioners_cross_reference
    - documentation for the G group
    - documentation for the positions group
    - documentation for other NXnote groups
    - the MCA group (now an NXnote) could be an NXdetector
    - clarify what items are defined from SPEC macros
    - clarify what items appear on a conditional basis
    - how to write and load a custom plugin

.. sidebar:: *for reference*: tree view

   In this documentation, the command [#punx]_::

       punx tree FILENAME.hdf5

   is used to generate a tree view of an HDF5 file's structure.

SPEC data files contain data from one or more measurements called *scans*. Each
scan is numbered (where the number is not necessarily unique within a data
file).  NeXus files are written [#]_ as HDF5 files with a tree structure [#]_
where the groups use the NeXus base class [#]_ definitions.

HDF5 files are binary (not human readable); in this documentation, the tree
structure (hierarchy) of the file will be shown.  Various terms are shown
symbolically, as described in the next table.

==================  ===============  ==================
symbolic            example          meaning
==================  ===============  ==================
``NAME:NXclass``    ``data:NXdata``  HDF5 name of group and NeXus base class used
``{NAME}``          ``scan_number``  name is chosen as described
``@{NAME}``         ``@default``     HDF5 attribute of the parent group or field [#NXfield]_
``NX_{datatype}``   ``NX_NUMBER``    NeXus data type [#NX_datatype]_
``NX_{unittype}``   ``NX_CHAR``      NeXus unit type [#NX_unittype]_
==================  ===============  ==================

The root level of the file uses the structure of the NeXus **NXroot** [#NXroot]_
base class.

.. index:: plugin
.. index:: ! tree structure - NeXus HDF5

Basic Tree Structure
--------------------

The basic tree structure of the NeXus HDF5 file is (where ``AXIS`` and
``SIGNAL`` are the names of the first and last columns, respectively, of the
scan and ``SCAN_N`` is the scan number from the scan's ``#S`` :index:`control line`
[#control_line]_ in the data file):

.. code-block::
   :linenos:

    FILE_NAME:NXroot
        @default="S{SCAN_N}"
        S{SCAN_N}:NXentry
            @default="data"
            data:NXdata
                @axes={AXIS}
                @signal={SIGNAL}
                {AXIS}:NX_NUMBER[n] = ... data ...
                {SIGNAL}:NX_NUMBER[n] = ... data ...

A NeXus **NXentry** [#NXentry]_ group will be created for each scan to be
written.  The name of the group is composed from the scan number (``SCAN_N``) as
``S{SCAN_N}`` (such as ``S1`` for ``SCAN_N=1``).  If there is more than one scan
``#S 1`` in the data file, there may be an additional decimal point and then a
sequence number indicating the specific (such as ``S1``, ``S1.1`` and ``S1.2``
for the first, second, and third scans, respectively, with ``#S 1``)

The scan data will be placed in a **NXdata** [#NXdata]_ group named
``data`` below the **NXentry** group. Other information from the scan will be
written as described in the sections below. There are variations on the tree
structure as the complexity of a scan increases. Examples of such variation
include:

* multi-axis scans
* multiple detectors
* 2-D and higher dimensionality data (such as mesh scans)
* multi-channel detectors
* custom metadata
* comments

Example 1-D scan
++++++++++++++++

This SPEC data file (where for brevity of this example, additional content has
been removed):

.. code-block::
   :linenos:

    #F /home/sricat/POLAR/data/CMR/lmn40.spe
    #E 918630612
    #D Wed Feb 10 01:10:12 1999
    #C spec1ID  User = polar
    #O0    Theta  Two Theta  sample x  sample y

    #S 1  ascan  tth -0.7 -0.5  101 1
    #D Wed Feb 10 01:11:25 1999
    #T 1  (Seconds)
    #P0 -0.80000004 -0.60000003 -0.15875 0.16375
    #N 5
    #L Two Theta    Epoch  Seconds  ic0  winCZT
    -0.70000003  75 1 340592 1
    -0.69812503  76 1 340979 1
    -0.69612503  78 1 341782 1
    -0.69412503  79 1 342594 1
    -0.69212503  80 1 343300 0
    -0.69012503  82 1 341851 0
    -0.68812503  83 1 342126 1
    -0.68612503  85 1 342311 0
    -0.68425003  86 1 343396 1
    -0.68225003  88 1 343772 1
    -0.68025003  89 1 343721 1
    -0.67825003  91 1 341127 2
    -0.67625003  92 1 343733 0
    #C Wed Feb 10 01:12:39 1999.  More scan content removed for brevity.

is written to a NeXus HDF5 file.  The NeXus HDF5 file has this tree structure
(for brevity, additional structure has been removed):

.. code-block::
   :linenos:

   @default = "S1"
   S1:NXentry
     @default = "data"
     data:NXdata
       @axes = "Two_Theta"
       @signal = "winCZT"
       Epoch:NX_FLOAT64[13] = [75.0, 76.0, 78.0, '...', 92.0]
         @spec_name = "Epoch"
       Seconds:NX_FLOAT64[13] = [1.0, 1.0, 1.0, '...', 1.0]
         @spec_name = "Seconds"
       Two_Theta:NX_FLOAT64[13] = [-0.70000003, -0.69812503, -0.69612503, '...', -0.67625003]
         @spec_name = "Two Theta"
       ic0:NX_FLOAT64[13] = [340592.0, 340979.0, 341782.0, '...', 343733.0]
         @spec_name = "ic0"
       winCZT:NX_FLOAT64[13] = [1.0, 1.0, 1.0, '...', 0.0]
         @spec_name = "winCZT"

SPEC Data File Contents
-----------------------

The SPEC data file is written to a NeXus HDF5 file by parts as described below.
The file name (shown in this example):

.. code-block::
   :linenos:

   #F /home/sricat/POLAR/data/CMR/lmn40.spe

The file name is copied to the file root as the ``SPEC_file`` attribute
(denoted here as ``@SPEC_file``):

.. code-block::
   :linenos:

   @SPEC_file = "/home/sricat/POLAR/data/CMR/lmn40.spe"

It is expected there is only one ``#F`` control line in a SPEC data file
(assumes that the name of a file will not change midway) and, if it appears, it
is the first line.

.. _data.file.header:

File header
+++++++++++

Some content from a SPEC data file header is written to the root of the NeXus
HDF5 file.  Consider this example:

.. code-block::
   :linenos:

   #E 918630612
   #D Wed Feb 10 01:10:12 1999
   #C spec1ID  User = polar
   #O0    Theta  Two Theta  sample x  sample y

From this example, these are written to attributes of the file root:

.. code-block::
   :linenos:

   @SPEC_epoch = 918630612
   @SPEC_date = "1999-02-10T01:10:12"
   @SPEC_comments = "spec1ID  User = polar"
   @SPEC_num_headers = 1

The additional information in the positioner names ``#O0`` control line will be
used later (in :ref:`data.file.positioners`) when writing the positioners to the
file. The ``@SPEC_comments`` includes *all* :ref:`data.file.comments` that
appear in the header section(s).

.. _data.file.scan:

Scan
++++

TODO:

.. _data.file.comments:

Comments
++++++++

These comments from a SPEC data file scan:

.. code-block::
   :linenos:

   #C Fri Mar 11 16:29:51 2022.  plan_type = generator
   #C Fri Mar 11 16:29:51 2022.  uid = dccc572d-9a5b-4f72-87d7-233b2fd33e4e
   #C Fri Mar 11 16:29:57 2022.  num_events_baseline = 2
   #C Fri Mar 11 16:29:57 2022.  num_events_primary = 10
   #C Fri Mar 11 16:29:57 2022.  exit_status = success

are written to the :ref:`data.file.scan` entry as a single NeXus *field*
[#NXfield]_ named ``comments`` where all the scan's comments are joined together
by newline (``\n``) characters:

.. code-block::
   :linenos:

   comments:NX_CHAR = [b'Fri Mar 11 16:29:51 2022.  plan_type = generator\nFri Mar 11 16:29:51 2022.  uid = dccc572d-9a5b-4f72-87d7-233b2fd33e4e\nFri Mar 11 16:29:57 2022.  num_events_baseline = 2\nFri Mar 11 16:29:57 2022.  num_events_primary = 10\nFri Mar 11 16:29:57 2022.  exit_status = success']

Note, when printed, the value of this example ``comments`` field looks like::

   Fri Mar 11 16:29:51 2022.  plan_type = generator
   Fri Mar 11 16:29:51 2022.  uid = dccc572d-9a5b-4f72-87d7-233b2fd33e4e
   Fri Mar 11 16:29:57 2022.  num_events_baseline = 2
   Fri Mar 11 16:29:57 2022.  num_events_primary = 10
   Fri Mar 11 16:29:57 2022.  exit_status = success

.. _data.file.counters:

Counters
++++++++

TODO: names and mnemonics

.. _data.file.positioners:

Positioners
+++++++++++

TODO: names and mnemonics

Diffractometer Configuration
++++++++++++++++++++++++++++

TODO:

Instruments
+++++++++++

TODO: names and mnemonics

Footnotes
---------

.. [#punx] Visualize NeXus file tree structure :
   https://prjemian.github.io/punx/tree.html#tree
.. [#] NeXus objects and terms:
   https://manual.nexusformat.org/design.html#nexus-objects-and-terms
.. [#] NeXus tree structure:
   https://manual.nexusformat.org/introduction.html#example-of-a-nexus-file
.. [#] NeXus groups (base classes):
   https://manual.nexusformat.org/classes/base_classes/
.. [#control_line] See :ref:`supplied_plugins` for a full list of the supported
   control lines provided with **spec2nexus**.
.. [#NX_datatype] List of NeXus data types:
   https://manual.nexusformat.org/nxdl-types.html#field-types-allowed-in-nxdl-specifications
.. [#NX_unittype] List of NeXus unit categories:
   https://manual.nexusformat.org/nxdl-types.html#unit-categories-allowed-in-nxdl-specifications
.. [#NXfield] A NeXus **field** is the same as an HDF5 **dataset**.  The rename is
   due to historical reasons in NeXus when XML was used as a back-end data file
   storage format.

NeXus base classes

.. [#NXdata] **NXdata**:   https://manual.nexusformat.org/classes/base_classes/NXdata.html
.. [#NXdetector] **NXdetector**:   https://manual.nexusformat.org/classes/base_classes/NXdetector.html
.. [#NXentry] **NXentry**:   https://manual.nexusformat.org/classes/base_classes/NXentry.html
.. [#NXinstrument] **NXinstrument**:   https://manual.nexusformat.org/classes/base_classes/NXinstrument.html
.. [#NXnote] **NXnote**:   https://manual.nexusformat.org/classes/base_classes/NXnote.html
.. [#NXpositioner] **NXpositioner**:   https://manual.nexusformat.org/classes/base_classes/NXpositioner.html
.. [#NXroot] **NXroot**:   https://manual.nexusformat.org/classes/base_classes/NXroot.html
.. [#NXsample] **NXsample**:   https://manual.nexusformat.org/classes/base_classes/NXsample.html
