
:mod:`spec2nexus.plugin`
########################

An extensible plug-in architecture is used to handle the different possible
control lines (such as **#F**, **#E**, **#S**, ...) in a SPEC data file.

Plugins can be used to parse or ignore certain control lines in SPEC data files.
Through this architecture, it is possible to support custom control lines, 
such as **#U** (SPEC standard control line for any user data).
One example is support for the :ref:`UNICAT-style <unicat_plugin>` of metadata 
provided in the scan header.

Plugins are now used to handle all control lines in :mod:`spec2nexus.pySpec`.
Any control line encountered but not recognized will raise a
:class:`~spec2nexus.pySpec.UnknownSpecFilePart` exception.


.. _supplied_plugins:

Supplied pySpec plugin modules
******************************

These plugin modules are supplied:

.. autosummary::
   :nosignatures:

   ~spec2nexus.control_lines.spec_common_pyspec
   ~spec2nexus.control_lines.unicat_pyspec
   ~spec2nexus.control_lines.uim_pyspec


.. toctree::
   :maxdepth: 2
   :hidden:
   :glob:

   supplied_plugins/*

Writing a custom plugin
***********************

.. toctree::
   :maxdepth: 2
   :glob:

   how_to_write_plugin


Overview of the supplied pySpec plugins
***************************************

Plugins for these control lines [#]_ are provided in **spec2nexus**:

.. autosummary::
   :nosignatures:

   ~spec2nexus.control_lines.spec_common_pyspec.SPEC_File
   ~spec2nexus.control_lines.spec_common_pyspec.SPEC_Epoch
   ~spec2nexus.control_lines.spec_common_pyspec.SPEC_Date
   ~spec2nexus.control_lines.spec_common_pyspec.SPEC_Comment
   ~spec2nexus.control_lines.spec_common_pyspec.SPEC_Geometry
   ~spec2nexus.control_lines.spec_common_pyspec.SPEC_NormalizingFactor
   ~spec2nexus.control_lines.spec_common_pyspec.SPEC_CounterNames
   ~spec2nexus.control_lines.spec_common_pyspec.SPEC_CounterMnemonics
   ~spec2nexus.control_lines.spec_common_pyspec.SPEC_Labels
   ~spec2nexus.control_lines.spec_common_pyspec.SPEC_Monitor
   ~spec2nexus.control_lines.spec_common_pyspec.SPEC_NumColumns
   ~spec2nexus.control_lines.spec_common_pyspec.SPEC_PositionerNames
   ~spec2nexus.control_lines.spec_common_pyspec.SPEC_PositionerMnemonics
   ~spec2nexus.control_lines.spec_common_pyspec.SPEC_Positioners
   ~spec2nexus.control_lines.spec_common_pyspec.SPEC_HKL
   ~spec2nexus.control_lines.spec_common_pyspec.SPEC_Scan
   ~spec2nexus.control_lines.spec_common_pyspec.SPEC_CountTime
   ~spec2nexus.control_lines.spec_common_pyspec.SPEC_TemperatureSetPoint
   ~spec2nexus.control_lines.spec_common_pyspec.SPEC_DataLine
   ~spec2nexus.control_lines.spec_common_pyspec.SPEC_MCA
   ~spec2nexus.control_lines.spec_common_pyspec.SPEC_MCA_Array
   ~spec2nexus.control_lines.spec_common_pyspec.SPEC_MCA_Calibration
   ~spec2nexus.control_lines.spec_common_pyspec.SPEC_MCA_ChannelInformation
   ~spec2nexus.control_lines.spec_common_pyspec.SPEC_MCA_CountTime
   ~spec2nexus.control_lines.spec_common_pyspec.SPEC_MCA_RegionOfInterest
   ~spec2nexus.control_lines.unicat_pyspec.UNICAT_MetadataMnemonics
   ~spec2nexus.control_lines.unicat_pyspec.UNICAT_MetadataValues
   ~spec2nexus.control_lines.uim_pyspec.UIM_generic

.. [#] Compare this list with :ref:`control_line_list`


source code documentation
*************************

.. automodule:: spec2nexus.plugin
    :members: 
    :synopsis: Define the plug-in architecture.
