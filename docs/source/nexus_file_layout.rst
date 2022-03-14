NeXus File Layout
#################

.. https://github.com/prjemian/spec2nexus/issues/192

    from spec2nexus import spec, writer
    sdf = spec.SpecDataFile("one-scan.dat")
    scans = sdf.getScanNumbersChronological()
    writer.Writer(sdf).save("one-scan.hdf5", scan_list=scans)
    !punx tree one-scan.hdf5

.. TODO:

    - documentation for counter_cross_reference
    - documentation for the G group
    - documentation for other NXnote groups
    - the MCA group (now an NXnote) could be an NXdetector
    - clarify what items are defined from SPEC macros
    - clarify what items appear on a conditional basis

.. sidebar:: *for reference*: tree view

   In this documentation, the command [#punx]_::

       punx tree FILENAME.hdf5

   is used to generate a tree view of an HDF5 file's structure.

SPEC data files contain data from one or more measurements called *scans*
written according to the **Standard Data-File Format**. [#spec.format]_  Each
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
``@{NAME}``         ``@default``     HDF5 attribute of the parent group or field [#NX.field]_
``NX_{datatype}``   ``NX_NUMBER``    uses this NeXus data type [#NX.datatype]_
``NX_{unittype}``   ``NX_CHAR``      uses this NeXus unit type [#NX.unittype]_
==================  ===============  ==================

.. index:: plugin
.. index:: ! tree structure - NeXus HDF5

Basic Tree Structure
--------------------

The basic tree structure of the NeXus HDF5 file is shown below:

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

.. sidebar:: ``NXroot``

   It is not required to write a ``NX_class="NXroot"`` attribute to the
   root of any NeXus data file.  In fact, it is very rare to find this attribute
   in any NeXus HDF5 file.  We only show it here for guidance in how to build
   a file using the NeXus standard.

The root level of the file uses the structure of the NeXus **NXroot** [#NXroot]_
base class.

The ``@default`` attribute points the way to the default plottable data.
See the NeXus documentation [#NX.default]_ for more details.

Here, ``AXIS`` and ``SIGNAL`` are the names of the first and last columns,
respectively, of the scan and ``SCAN_N`` is the scan number from the scan's
``#S`` :index:`control line` [#spec.format]_, [#control_line]_ in the data file.

A NeXus **NXentry** [#NXentry]_ group will be created for each scan to be
written.  See section :ref:`data.file.scan` below for more details.

.. sidebar:: image detectors

   SPEC data files do not usually contain data from a 2-D image
   detector.  A comment (or other control line such as ``#U``) may be used
   to describe the location of an external file containing such data
   and how to find the image frame from that file.  No standard
   pattern exists for SPEC data files to reference such images.

The scan data will be placed in a **NXdata** [#NXdata]_ group named ``data``
below the **NXentry** group.   See section :ref:`data.file.scan_data` below for
more details.

Other information from the scan will be written as described in the sections
below. There are variations on the tree structure as the complexity of a scan
increases. Examples of such variation include:

* multi-axis scans (such as ``a2scan``, ``a3scan``, ``a4scan``)
* multi-channel detectors
* 2-D and higher dimensionality scans (such as ``mesh``, ``hklmesh``, MCA)
* custom metadata
* comments

Example 1-D scan
++++++++++++++++

This SPEC data file (where for brevity of this example, additional content has
been removed) is a one-dimensional step scan of a counter named ``winCZT`` (last
column) versus a motor named ``Two Theta`` (first column) using a counting time
of 1 second per point. Data collection was configured to include data from an
additional counter named ``ic0``:

.. code-block::
   :linenos:

   #F /home/sricat/POLAR/data/CMR/lmn40.spe
   #E 918630612
   #D Wed Feb 10 01:10:12 1999
   #C spec1ID  User = polar
   #O0    Theta  Two Theta  sample x  sample y
   #o0 th tth samx samy

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

The SPEC data file is written to a NeXus HDF5 file with this tree structure (for
brevity, additional structure has been removed):

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

.. _data.file.name:

File name
+++++++++

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

.. FIXME: get instrument name from first #C? as SPEC_instrument?

From this example, this content is written to attributes of the file root:

.. code-block::
   :linenos:

   @SPEC_epoch = 918630612
   @SPEC_date = "1999-02-10T01:10:12"
   @SPEC_comments = "spec1ID  User = polar"
   @SPEC_user = "polar"
   @SPEC_num_headers = 1

The ``@SPEC_comments`` attribute includes contents of *all* ``#C`` (comment)
lines that appear in the header section(s), joined together by newline (``\n``)
characters. See :ref:`data.file.comments` for how this handled in scans.

The additional information in the positioner names ``#O0`` control line will be
used later (in :ref:`data.file.positioners`) when writing the positioners to the
file.

.. _data.file.scan:

Scan
++++

The ``#S`` control line marks the beginning of each scan in a SPEC data file.
It provides the scan number (``SCAN_N`` in SPEC) and the scan command.  Consider
this example:

.. code-block::
   :linenos:

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

From this example, this structure (from ``#S``, ``#D``, ``#T``, and ``#C``
control lines) is written as a new **NXentry** [#NXentry] group at the root of
the NeXus HDF5 file:

.. code-block::
   :linenos:

   S1:NXentry
     @NX_class = "NXentry"
     @default = "data"
     T:NX_FLOAT64 = 1.0
       @description = "SPEC scan with constant counting time"
       @units = "s"
     command:NX_CHAR = [b'ascan  tth -0.7 -0.5  101 1']
     comments:NX_CHAR = [b'Wed Feb 10 01:12:39 1999.  More scan content removed for brevity.']
     counting_basis:NX_CHAR = [b'SPEC scan with constant counting time']
     date:NX_CHAR = [b'1999-02-10T01:11:25']
     experiment_description:NX_CHAR = [b'SPEC scan']
       @description = "SPEC data file scan"
     scan_number:NX_INT64 = 1
       @spec_name = "SCAN_N"
     title:NX_CHAR = [b'1  ascan  tth -0.7 -0.5  101 1']

The name of the group is composed from the scan number (``SCAN_N``) as::

   S{SCAN_N}

(such as ``S1`` for ``SCAN_N=1``).

If there is more than one scan with the same ``SCAN_N`` (such as ``#S 1``) in
the data file, the *additional scans* will be named with an additional decimal
point and then a sequence number (described here as ``REPEAT_NUMBER``)
indicating the specific repeat::

   S{SCAN_N}.{REPEAT_NUMBER}

(such as ``S1``, ``S1.1`` and ``S1.2`` for the first, second, and third scans,
respectively, with ``#S 1``) The :ref:`data.file.scan_data` will be described in
the next section.

Note that ``command`` and ``title`` are almost* the same content but not exactly
the same.  The difference is that ``command`` is the ``title`` with the scan
number removed from the beginning.

.. _data.file.scan_data:

Scan Data
+++++++++

Consider the SPEC scan data shown in section :ref:`data.file.scan` above.  The
``#L``, ``#N``, ``#M``, ``#T``, and data lines (those with no ``#`` at the start
of the line) are written as a new **NXdata** [#NXdata]_ group as a child of the scan
group (**NXentry**) of the NeXus HDF5 file:

.. code-block::
   :linenos:

   data:NXdata
     @NX_class = "NXdata"
     @Two_Theta_indices = [0]
     @axes = "Two_Theta"
     @description = "SPEC scan data"
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

.. TODO: describe this

.. _data.file.positioners:

Positioners
+++++++++++

Consider the SPEC scan data shown in section :ref:`data.file.scan` above,
associated with the scan header data shown in section :ref:`data.file.header`.
The ``#O`` lines in the header provide the *names* of the positioners while the
``#P`` lines report the positioner values at the start of the scan. The lines
are numbered with a sequential index (starting at ``0``) to keep the line
lengths within page limits. When present (such as this example), the ``#o``
lines provide the *mnemonic* (also known as *mne*) names corresponding to the
positioner names from the ``#O`` lines.

The data from the ``#O`` and ``#P`` lines is written to a **NXnote**
[#NXnote]_ group named ``positioners``.
The ``positioners`` group is written as a child of the scan group (**NXentry**)
of the NeXus HDF5 file.
This group is also linked to the ``instrument`` group. [#NXinstrument]_ See the
:ref:`data.file.instrument` section below.

Each positioner (name and value) is written to a **NXpositioner**
[#NXpositioner]_ group with a name derived (via
:func:`~spec2nexus.utils.clean_name()`) from the name provided in the SPEC scan.
_This change of names ensures the field names in the NeXus HDF5 file conform to
the NeXus standard. [#NX.naming.datarules]  If the SPEC menmonic is available in
the data file, it is also written as a ``@spec_mne`` attribute with both the
``name`` and ``value`` fields. The **NXpositioner** groups are written as
children of the ``positioners`` group.

.. index:: units

.. note:: Engineering units are not written

   No ``@units`` attribute is provided for any of the values written by
   **spec2nexus** (except where provided by custom support). SPEC data files do
   not provide the engineering units for any of the values and it is not
   possible to guess the appropriate type of units [#NX.unittype]_ to use. The
   NeXus documentation about data units [#NX.units.datarules]_ states:

      ... any field must have a units attribute which describes the units.

   yet this is not a strict requirement.  (The ``@units`` attribute is not marked
   required in the NeXus NXDL schema.)

.. code-block::
   :linenos:

   positioners:NXnote
      @NX_class = "NXnote"
      @description = "SPEC positioners (#P & #O lines)"
      @target = "/S1/positioners"
      Theta:NXpositioner
        @NX_class = "NXpositioner"
        name:NX_CHAR = [b'Theta']
          @spec_mne = "th"
          @spec_name = "Theta"
        value:NX_FLOAT64 = -0.80000004
          @spec_mne = "th"
          @spec_name = "Theta"
      Two_Theta:NXpositioner
        @NX_class = "NXpositioner"
        name:NX_CHAR = [b'Two_Theta']
          @spec_mne = "tth"
          @spec_name = "Two Theta"
        value:NX_FLOAT64 = -0.60000003
          @spec_mne = "tth"
          @spec_name = "Two Theta"
      sample_x:NXpositioner
        @NX_class = "NXpositioner"
        name:NX_CHAR = [b'sample_x']
          @spec_mne = "samx"
          @spec_name = "sample x"
        value:NX_FLOAT64 = -0.15875
          @spec_mne = "samx"
          @spec_name = "sample x"
      sample_y:NXpositioner
        @NX_class = "NXpositioner"
        name:NX_CHAR = [b'sample_y']
          @spec_mne = "samy"
          @spec_name = "sample y"
        value:NX_FLOAT64 = 0.16375
          @spec_mne = "samy"
          @spec_name = "sample y"

When the ``#o`` lines are present in the scan's header, a **NXnote** [#NXnote]_
group named ``positioner_cross_reference`` is written as a child of the scan
group (**NXentry**) of the NeXus HDF5 file.  This group describes a
cross-reference between the *field* names of the ``positioner`` group and the
positioner names used in the SPEC scan.

.. code-block::
   :linenos:

   positioner_cross_reference:NXnote
      @NX_class = "NXnote"
      @comment = "keys are SPEC positioner mnemonics, values are SPEC positioner names"
      @description = "cross-reference SPEC positioner mnemonics and names"
      samx:NX_CHAR = [b'sample x']
        @field_name = "sample_x"
        @mne = "samx"
      samy:NX_CHAR = [b'sample y']
        @field_name = "sample_y"
        @mne = "samy"
      th:NX_CHAR = [b'Theta']
        @field_name = "Theta"
        @mne = "th"
      tth:NX_CHAR = [b'Two Theta']
        @field_name = "Two_Theta"
        @mne = "tth"

.. _data.file.counters:

Counters
++++++++

#J & #j

TODO: names and mnemonics

TODO: counter_cross_reference

.. _data.file.geometry:

Geometry
++++++++

Diffractometer Configuration and sample orientation

#G & #Q

TODO:

.. _data.file.instrument:

Instrument
++++++++++

TODO:

.. code-block::
   :linenos:

   instrument:NXinstrument
     @NX_class = "NXinstrument"
     positioners --> /S1/positioners

.. _data.file.comments:

Comments
++++++++

These comments from an example SPEC data file scan:

.. code-block::
   :linenos:

   #C Fri Mar 11 16:29:51 2022.  plan_type = generator
   #C Fri Mar 11 16:29:51 2022.  uid = dccc572d-9a5b-4f72-87d7-233b2fd33e4e
   #C Fri Mar 11 16:29:57 2022.  num_events_baseline = 2
   #C Fri Mar 11 16:29:57 2022.  num_events_primary = 10
   #C Fri Mar 11 16:29:57 2022.  exit_status = success

are written to the :ref:`data.file.scan` entry as a single NeXus *field*
[#NX.field]_ named ``comments`` where all the scan's comments are joined together
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

.. _data.file.metadata:

Metadata
++++++++

TODO:  #U and other (#H/#V, #UXML, ...)

Footnotes
---------

.. [#spec.format] SPEC **Standard Data-File Format** :
   https://certif.com/spec_manual/mac_3_13.html
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
.. [#NX.datatype] List of NeXus data types:
   https://manual.nexusformat.org/nxdl-types.html#field-types-allowed-in-nxdl-specifications
.. [#NX.units.datarules] https://manual.nexusformat.org/datarules.html#design-units
.. [#NX.naming.datarules] https://manual.nexusformat.org/datarules.html#naming-conventions
.. [#NX.unittype] List of NeXus unit categories:
   https://manual.nexusformat.org/nxdl-types.html#unit-categories-allowed-in-nxdl-specifications
.. [#NX.field] A NeXus **field** is the same as an HDF5 **dataset**.  The rename is
   due to historical reasons in NeXus when XML was used as a back-end data file
   storage format.
.. [#NX.default] Used to identify the default plottable data in a NeXus HDF5 file.
   https://manual.nexusformat.org/datarules.html#version-3

NeXus base classes

.. [#NXdata] **NXdata**:   https://manual.nexusformat.org/classes/base_classes/NXdata.html
.. [#NXdetector] **NXdetector**:   https://manual.nexusformat.org/classes/base_classes/NXdetector.html
.. [#NXentry] **NXentry**:   https://manual.nexusformat.org/classes/base_classes/NXentry.html
.. [#NXinstrument] **NXinstrument**:   https://manual.nexusformat.org/classes/base_classes/NXinstrument.html
.. [#NXnote] **NXnote**:   https://manual.nexusformat.org/classes/base_classes/NXnote.html
.. [#NXpositioner] **NXpositioner**:   https://manual.nexusformat.org/classes/base_classes/NXpositioner.html
.. [#NXroot] **NXroot**:   https://manual.nexusformat.org/classes/base_classes/NXroot.html
.. [#NXsample] **NXsample**:   https://manual.nexusformat.org/classes/base_classes/NXsample.html
