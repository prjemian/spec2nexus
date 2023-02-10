.. _data.file.counters:

Counters
++++++++

SPEC data file header control lines ``#J`` and ``#j`` describe the relationship
between counter names (``#J``) and mnemonics (``#j``).  The lines
are numbered with a sequential index (starting at ``0``) to keep the line
lengths within page limits.

When both types are present in the scan's header, such as this example:

.. code-block::
   :linenos:

   #J0 seconds  I0  I00  USAXS_PD  TR_diode
   #j0 sec I0 I00 upd2 trd

then ``/SCAN/counter_cross_reference`` (a **NXnote** [#NXnote]_ group) is
written.  The fields of the group are the mnemonics and the values are the
names.

.. code-block::
   :linenos:

   counter_cross_reference:NXnote
      @NX_class = "NXnote"
      @comment = "keys are SPEC counter mnemonics, values are SPEC counter names"
      @description = "cross-reference SPEC counter mnemonics and names"
      I0:NX_CHAR = [b'I0']
      I00:NX_CHAR = [b'I00']
      sec:NX_CHAR = [b'seconds']
      trd:NX_CHAR = [b'TR_diode']
      upd2:NX_CHAR = [b'USAXS_PD']

.. [#NXnote] **NXnote**:   https://manual.nexusformat.org/classes/base_classes/NXnote.html
