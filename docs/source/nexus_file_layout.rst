NeXus File Layout
#################

.. https://github.com/prjemian/spec2nexus/issues/192

    from spec2nexus import spec, writer
    sdf = spec.SpecDataFile("one-scan.dat")
    scans = sdf.getScanNumbersChronological()
    writer.Writer(sdf).save("one-scan.hdf5", scan_list=scans)
    !punx tree one-scan.hdf5

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
``@{NAME}``         ``@default``     HDF5 attribute of the parent group or field
``NX_{datatype}``   ``NX_NUMBER``    NeXus data type [#NX_datatype]_
``NX_{unittype}``   ``NX_NUMBER``    NeXus unit type [#NX_unittype]_
==================  ===============  ==================

.. TODO: maybe use a table?
.. TODO: describe the ``NAME:NXclass`` syntax
.. TODO: describe the ``{NAME}`` syntax
.. TODO: describe the ``@`` syntax
.. TODO: describe the ``NX_type`` terms (data types)

The root level of the file uses the structure of the NeXus **NXroot** [#NXroot]_
base class.

Basic Tree Structure
--------------------

The basic tree structure of the NeXus HDF5 file is (where ``AXIS`` and
``SIGNAL`` are the names of the first and last columns, respectively, of the
scan and ``SCAN_N`` is the scan number from the scan's ``#S`` control line in
the data file)::

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

.. TODO: might be better to show a scan written by SPEC

This SPEC data file (where for brevity of this example, additional content has
been removed)::

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

is written to a NeXus/HDF5 file with this tree structure (for brevity,
additional structure has been removed)::

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

Comments
-----------

TODO:

Counters (Detectors)
----------------------

TODO: names and mnemonics

Positioners
-----------

TODO: names and mnemonics

Diffractometer Configuration
----------------------------

TODO:

Instrument
----------------------

TODO: names and mnemonics

Footnotes
---------

.. [#] NeXus objects and terms:
   https://manual.nexusformat.org/design.html#nexus-objects-and-terms
.. [#] NeXus tree structure:
   https://manual.nexusformat.org/introduction.html#example-of-a-nexus-file
.. [#] NeXus groups (base classes):
   https://manual.nexusformat.org/classes/base_classes/
.. [#NX_datatype] List of NeXus data types:
   https://manual.nexusformat.org/nxdl-types.html#field-types-allowed-in-nxdl-specifications
.. [#NX_unittype] List of NeXus unit categories:
   https://manual.nexusformat.org/nxdl-types.html#unit-categories-allowed-in-nxdl-specifications

NeXus base classes

.. [#NXdata] **NXdata**:   https://manual.nexusformat.org/classes/base_classes/NXdata.html
.. [#NXentry] **NXentry**:   https://manual.nexusformat.org/classes/base_classes/NXentry.html
.. [#NXinstrument] **NXinstrument**:   https://manual.nexusformat.org/classes/base_classes/NXinstrument.html
.. [#NXnote] **NXnote**:   https://manual.nexusformat.org/classes/base_classes/NXnote.html
.. [#NXpositioner] **NXpositioner**:   https://manual.nexusformat.org/classes/base_classes/NXpositioner.html
.. [#NXroot] **NXroot**:   https://manual.nexusformat.org/classes/base_classes/NXroot.html
.. [#NXsample] **NXsample**:   https://manual.nexusformat.org/classes/base_classes/NXsample.html
