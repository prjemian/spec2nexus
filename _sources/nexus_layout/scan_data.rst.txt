.. _data.file.scan_data:

Scan Data
+++++++++

Consider the SPEC scan data shown in section :ref:`data.file.scan` above.  The
``#L``, ``#N``, ``#M``, ``#T``, and data lines (those with no ``#`` at the start
of the line) are written to ``/SCAN/data`` (a **NXdata** [#NXdata]_ group):

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

A field [#NX.field]_ is created for each column of data.  Generally, data rows
for a scan do not start with a ``#`` sign and are provided after the data labels
in the ``#L`` row.  (The ``#N`` row tells how many columns are provided in the
scan.) The name of each column is converted (via
:func:`~spec2nexus.utils.clean_name()`) to a field name that conforms to the
NeXus standard. [#NX.naming.datarules]_  The original column name is provided
by the ``@spec_name`` attribute.

.. [#NXdata] **NXdata**:   https://manual.nexusformat.org/classes/base_classes/NXdata.html
.. [#NX.field] A NeXus **field** is the same as an HDF5 **dataset**.  The rename is   due to historical reasons in NeXus when XML was used as a back-end data file   storage format.
.. [#NX.naming.datarules] https://manual.nexusformat.org/datarules.html#naming-conventions
