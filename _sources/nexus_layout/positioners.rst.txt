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

The data from the ``#O`` and ``#P`` lines is written to ``/SCAN/positioners`` (a
**NXnote** [#NXnote]_ group). ``/SCAN/positioners`` is also linked to
``/SCAN/instrument/positioners``. See the :ref:`data.file.instrument` section
below.

Within the ``/SCAN/positioners/`` group, each positioner (name and value) is
written to a ``/SCAN/positioners/CLEAN_NAME`` **NXpositioner** [#NXpositioner]_
group.  ``CLEAN_NAME`` is derived (via
:func:`~spec2nexus.utils.clean_name(spec_positioner_name)`). This change of
names ensures the field [#NX.field]_ names in the NeXus HDF5 file conform to the
NeXus standard. [#NX.naming.datarules]_

If the SPEC menmonic for the positioner is available in the data file (from the
``#o`` control lines), it is also written as a ``@spec_mne`` attribute with both
the ``name`` and ``value`` fields.

.. index:: units

.. note:: Engineering units are not written

   Generally, the ``@units`` attribute is not provided for any of the values
   written by **spec2nexus** (except where provided by custom support or for
   diffractometers as described later in section :ref:`data.file.geometry`).
   SPEC data files do not provide the engineering units for any of the values
   and it is not possible to guess the appropriate type of units [#NX.unittype]_
   to use. The NeXus documentation about data units [#NX.units.datarules]_
   states:

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

When the ``#o`` lines are present in the scan's header, a cross-reference
between mnemonic and name is written in ``/SCAN/positioner_cross_reference`` (a
**NXnote** [#NXnote]_ group).  This group describes a cross-reference between
the *field* names of the ``positioner`` group and the positioner names used in
the SPEC scan.

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

.. [#NXnote] **NXnote**:   https://manual.nexusformat.org/classes/base_classes/NXnote.html
.. [#NXpositioner] **NXpositioner**:   https://manual.nexusformat.org/classes/base_classes/NXpositioner.html
.. [#NX.field] A NeXus **field** is the same as an HDF5 **dataset**.  The rename is   due to historical reasons in NeXus when XML was used as a back-end data file   storage format.
.. [#NX.naming.datarules] https://manual.nexusformat.org/datarules.html#naming-conventions
.. [#NX.unittype] List of NeXus unit categories:   https://manual.nexusformat.org/nxdl-types.html#unit-categories-allowed-in-nxdl-specifications
.. [#NX.units.datarules] https://manual.nexusformat.org/datarules.html#design-units
