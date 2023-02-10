.. _data.file.metadata:

Metadata
++++++++

Metadata in SPEC data files may be described using various
control lines.  The following table describes how each
control line is handled and written in a NeXus/HDF5 data file.

================  ================================
control line      section
================  ================================
``#R``            :ref:`data.file.metadata.R`
``#U``            :ref:`data.file.metadata.U`
``#H`` & ``#V``   :ref:`data.file.metadata.HV`
``#UXML``         :ref:`data.file.metadata.UXML`
================  ================================

.. _data.file.metadata.R:

SPEC UserResults
----------------------------------------

The SPEC data file header control line ``#R`` is reserved [#SPEC_control_lines]_
for users to describe any information of their choosing.  This control line may
be used in a scan.  It is optional but may be appear more than once.  Here are
examples from various SPEC data files:

.. code-block::
   :linenos:

   #R 2
   #R 11  Max: 83356  at 5.469   FWHM: 0.0165099  at 5.48551   COM: 5.48525   SUM: 3.47646e+06

When present in a scan, then ``/SCAN/UserResults`` (a **NXnote** [#NXnote]_
group) is created.  The value is written **as text** (any leading or trailing
white space is removed) into a field within this group as ``item_1`` (where the
number increments for each item in the scan).  Here is the ``UserResults`` group
created by the above example ``#R`` lines:

.. code-block::
   :linenos:

   UserResults:NXnote
      @NX_class = "NXnote"
      item_1:NX_CHAR = [b'2']
      item_2:NX_CHAR = [b'11  Max: 83356  at 5.469   FWHM: 0.0165099  at 5.48551   COM: 5.48525   SUM: 3.47646e+06']

.. _data.file.metadata.U:

SPEC UserReserved
----------------------------------------

The SPEC data file header control line ``#U`` is reserved [#SPEC_control_lines]_
for users to describe any information of their choosing.  This control line may
be used in both the header and a scan.  It is optional but may be appear more
than once.  Here are examples from various SPEC data files:

**header**

.. code-block::
   :linenos:

   #U p09user

**scan**

.. code-block::
   :linenos:

   #U Beam Current: 101.9
   #U Energy: 5.5000
   #U  EntSlits:  1.000 x  1.000 @  0.000, 37.775
   #U Undulator Tracking is on; Offset:0.070

When present in either the scan or its header, then ``/SCAN/UserReserved`` (a
**NXnote** [#NXnote]_ group) is created.  The value is written **as text** (any
leading or trailing white space is removed) into a field within this group as
``header_1`` or ``item_1`` (where the number increments for each item in
the header or scan, respectively).  Here is the ``UserReserved`` group created
by the above example ``#U`` lines:

.. code-block::
   :linenos:

   UserReserved:NXnote
      @NX_class = "NXnote"
      header_1:NX_CHAR = [b'p09user']
      item_1:NX_CHAR = [b'Beam Current: 101.9']
      item_2:NX_CHAR = [b'Energy: 5.5000']
      item_3:NX_CHAR = [b'EntSlits:  1.000 x  1.000 @  0.000, 37.775']
      item_4:NX_CHAR = [b'Undulator Tracking is on; Offset:0.070']

.. _data.file.metadata.HV:

UNICAT-style metadata
----------------------------------------

UNICAT-style metadata consists of key:value pairs encoded using the ``#H`` and
``#V`` control lines which describe keys and values, respectively.  The design
is similar to that used to describe positioner, using ``#O`` and ``#P`` lines
for the keys and values.  The keys are provided in the header, in numbered lines
``#H0``, ``#H1``, ... with multiple keys on a line.  The corresponding values
are provided on numbered ``#V`` lines in the scan, with matching number of
values on each line.  For example:

**header**

.. code-block::
   :linenos:

   #H0  SR_current  barometer_mbar
   #H1  SR_BPM_HP  SR_BPM_VP  SR_BPM_HA  SR_BPM_VA
   #H2  DCM_energy  DCM_lambda  UND_energy  UND_tracking  UND_offset  mrEnc  arEnc

**scan**

.. code-block::
   :linenos:

   #V0 102.23 981.665
   #V1 -0.0201432 0.110706 28.0838 11.7067
   #V2 18 0.688801 18.1723 1 0.2 10.4046 10.318091

When present in a scan, then ``/SCAN/metadata`` (a **NXnote** [#NXnote]_ group)
is created.  Within this group, a field is written for each key:value pair. It
may be necessary to change the name of a key, to make it unique, so all fields
will have the original name of the key written as the ``spec_name`` attribute.
Here is the ``metadata`` group created by the above example ``#H`` and ``#V``
lines:

.. code-block::
   :linenos:

   metadata:NXnote
      @NX_class = "NXnote"
      @description = "SPEC metadata (UNICAT-style #H & #V lines)"
      @target = "/S1/metadata"
      DCM_energy:NX_FLOAT64 = 18.0
        @spec_name = "DCM_energy"
      DCM_lambda:NX_FLOAT64 = 0.688801
        @spec_name = "DCM_lambda"
      SR_BPM_HA:NX_FLOAT64 = 28.0838
        @spec_name = "SR_BPM_HA"
      SR_BPM_HP:NX_FLOAT64 = -0.0201432
        @spec_name = "SR_BPM_HP"
      SR_BPM_VA:NX_FLOAT64 = 11.7067
        @spec_name = "SR_BPM_VA"
      SR_BPM_VP:NX_FLOAT64 = 0.110706
        @spec_name = "SR_BPM_VP"
      SR_current:NX_FLOAT64 = 102.23
        @spec_name = "SR_current"
      UND_energy:NX_FLOAT64 = 18.1723
        @spec_name = "UND_energy"
      UND_offset:NX_FLOAT64 = 0.2
        @spec_name = "UND_offset"
      UND_tracking:NX_FLOAT64 = 1.0
        @spec_name = "UND_tracking"
      arEnc:NX_FLOAT64 = 10.318091
        @spec_name = "arEnc"
      barometer_mbar:NX_FLOAT64 = 981.665
        @spec_name = "barometer_mbar"
      mrEnc:NX_FLOAT64 = 10.4046
        @spec_name = "mrEnc"

See section :ref:`unicat_plugin` for the API documentation.

.. _data.file.metadata.UXML:

UXML
----------------------------------------

See section :ref:`uxml_plugin` for more details about the ``#UXML`` control line
and the API documentation.  The ``#UXML`` lines provide an XML document
description in a scan's metadata. It is used at APS sector 33 but not so
much elsewhere.

----------------------------------------

.. [#SPEC_control_lines] https://certif.com/spec_help/scans.html
.. [#NXnote] **NXnote**:   https://manual.nexusformat.org/classes/base_classes/NXnote.html

