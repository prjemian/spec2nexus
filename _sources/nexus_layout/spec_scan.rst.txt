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
control lines) is written to a new **NXentry** [#NXentry]_ group at
the root of the NeXus HDF5 file:

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

.. sidebar:: ``/SCAN``

   We use ``/SCAN`` as a symbolic HDF5 address to refer to the *scan* entry of
   the NeXus data file. It means use the name formatted as described below
   (``S{SCAN_N}[.{REPEAT_NUMBER}]``) to identify this scan uniquely in a NeXus
   HDF5 data file.  Such as ``/S`` and ``/S1.1`` refer, respectively, to the
   first and second scans with the ``#S 1`` control line.

The name of the group (``/SCAN``) is composed from the scan number (``SCAN_N``) as::

   S{SCAN_N}[.{REPEAT_NUMBER}]

If there is more than one scan with the same ``SCAN_N`` (such as ``#S 1``) in
the data file, the *additional scans* will be named with an additional decimal
point and then a sequence number (described here as ``REPEAT_NUMBER``)
indicating the specific repeat, (such as ``S1``, ``S1.1`` and ``S1.2`` for the
first, second, and third scans, respectively, with ``#S 1``)

The :ref:`data.file.scan_data` will be described in the next section.

Note that ``command`` and ``title`` are *almost* the same content but not
*exactly* the same.  The difference is that ``command`` is the ``title`` with
the scan number removed from the beginning.

If the scan uses a constant monitor count (instead of a fixed time interval),
then the ``#T`` line in the scan is replaced by ``#M`` line, such as:

.. code-block::
   :linenos:

   #M 20000  (I0)

In the NeXus HDF5 file, the ``T`` field [#NX.field]_ is replaced by ``M``

.. code-block::
   :linenos:

   M:NX_FLOAT64 = 20000.0
      @description = "SPEC scan with constant monitor count"
      @units = "counts"
   monitor:NXmonitor
      @NX_class = "NXmonitor"
      preset --> /S1/M

.. [#NXentry] **NXentry**:   https://manual.nexusformat.org/classes/base_classes/NXentry.html
.. [#NX.field] A NeXus **field** is the same as an HDF5 **dataset**.  The rename is   due to historical reasons in NeXus when XML was used as a back-end data file   storage format.
