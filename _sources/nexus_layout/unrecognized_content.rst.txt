.. _data.file.unrecognized:

Unrecognized Control Line
++++++++++++++++++++++++++

Any control line that is not recognized by a plugin (see :ref:`plugin_list`)
will be written to a **NXnote** [#NXnote]_ group named ``unrecognized_{N}``
(where ``{N}``) is a numbered index starting at ``1``. (The algorithm looks for
the first available name not already used.)  Each unrecognized control line will
be added to this group in a separate field. Here is an example from a SPEC data
file with two such lines:

.. code-block::
   :linenos:

   # this line will not be recognized

   # another one

and how that content is represented in the NeXus HDF5 file:

.. code-block::
   :linenos:

   unrecognized_1:NXnote
      @NX_class = "NXnote"
      @description = "SPEC data file control lines not otherwise recognized"
      u0:NX_CHAR = [b'# this line will not be recognized']
        @spec_name = "u0"
      u1:NX_CHAR = [b'# another one']
        @spec_name = "u1"

.. [#NXnote] **NXnote**:   https://manual.nexusformat.org/classes/base_classes/NXnote.html
