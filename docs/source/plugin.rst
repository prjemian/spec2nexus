
:mod:`spec2nexus.plugin`
########################

An extensible plug-in architecture is used to handle the different possible
control lines (such as **#F**, **#E**, **#S**, ...) in a SPEC data file.

Plugins can be used to parse or ignore certain control lines in SPEC data files.
Through this architecture, it is possible to support custom control lines, 
such as **#U** (SPEC standard control line for any user data).
One example is support for the :ref:`UNICAT-style <unicat_plugin>` of metadata 
provided in the scan header.

Plugins are now used to handle all control lines in :mod:`spec2nexus.spec`.
Any control line encountered but not recognized will be placed as text
in a NeXus **NXnote** group named ``unrecognized``.

.. _supplied_plugins:

Supplied **spec** plugin modules
********************************

These plugin modules are supplied:

.. autosummary::
   :nosignatures:
   
   ~spec2nexus.plugins.spec_common_spec2nexus
   ~spec2nexus.plugins.fallback_spec2nexus
   ~spec2nexus.plugins.unicat_spec2nexus
   ~spec2nexus.plugins.uim_spec2nexus
   ~spec2nexus.plugins.XPCS_spec2nexus
   
.. toctree::
   :maxdepth: 2
   :hidden:
   :glob:

   supplied_plugins/*

Writing a custom plugin
***********************

While **spec2nexus** provides a comprehensive set of plugins
to handle the common SPEC control lines, custom control lines
are used at many facilities to write additional scan data
and scan metadata into the SPEC data file.  Custom plugins
are written to process these additions.

.. toctree::
   :maxdepth: 2
   :glob:

   how_to_write_plugin


Overview of the supplied **spec** plugins
*****************************************

Plugins for these control lines [#]_ are provided in **spec2nexus**:

.. autosummary::
   :nosignatures:

   ~spec2nexus.plugins.spec_common_spec2nexus.SPEC_File
   ~spec2nexus.plugins.spec_common_spec2nexus.SPEC_Epoch
   ~spec2nexus.plugins.spec_common_spec2nexus.SPEC_Date
   ~spec2nexus.plugins.spec_common_spec2nexus.SPEC_Comment
   ~spec2nexus.plugins.spec_common_spec2nexus.SPEC_Geometry
   ~spec2nexus.plugins.spec_common_spec2nexus.SPEC_NormalizingFactor
   ~spec2nexus.plugins.spec_common_spec2nexus.SPEC_CounterNames
   ~spec2nexus.plugins.spec_common_spec2nexus.SPEC_CounterMnemonics
   ~spec2nexus.plugins.spec_common_spec2nexus.SPEC_Labels
   ~spec2nexus.plugins.spec_common_spec2nexus.SPEC_Monitor
   ~spec2nexus.plugins.spec_common_spec2nexus.SPEC_NumColumns
   ~spec2nexus.plugins.spec_common_spec2nexus.SPEC_PositionerNames
   ~spec2nexus.plugins.spec_common_spec2nexus.SPEC_PositionerMnemonics
   ~spec2nexus.plugins.spec_common_spec2nexus.SPEC_Positioners
   ~spec2nexus.plugins.spec_common_spec2nexus.SPEC_HKL
   ~spec2nexus.plugins.spec_common_spec2nexus.SPEC_Scan
   ~spec2nexus.plugins.spec_common_spec2nexus.SPEC_CountTime
   ~spec2nexus.plugins.spec_common_spec2nexus.SPEC_UserReserved
   ~spec2nexus.plugins.spec_common_spec2nexus.SPEC_TemperatureSetPoint
   ~spec2nexus.plugins.spec_common_spec2nexus.SPEC_DataLine
   ~spec2nexus.plugins.spec_common_spec2nexus.SPEC_MCA
   ~spec2nexus.plugins.spec_common_spec2nexus.SPEC_MCA_Array
   ~spec2nexus.plugins.spec_common_spec2nexus.SPEC_MCA_Calibration
   ~spec2nexus.plugins.spec_common_spec2nexus.SPEC_MCA_ChannelInformation
   ~spec2nexus.plugins.spec_common_spec2nexus.SPEC_MCA_CountTime
   ~spec2nexus.plugins.spec_common_spec2nexus.SPEC_MCA_RegionOfInterest
   ~spec2nexus.plugins.fallback_spec2nexus.UnrecognizedControlLine
   ~spec2nexus.plugins.unicat_spec2nexus.UNICAT_MetadataMnemonics
   ~spec2nexus.plugins.unicat_spec2nexus.UNICAT_MetadataValues
   ~spec2nexus.plugins.uim_spec2nexus.UIM_generic
   ~spec2nexus.plugins.XPCS_spec2nexus.XPCS_VA
   ~spec2nexus.plugins.XPCS_spec2nexus.XPCS_VD
   ~spec2nexus.plugins.XPCS_spec2nexus.XPCS_VE

.. [#] Compare this list with :ref:`plugin_list`

source code documentation
*************************

.. automodule:: spec2nexus.plugin
    :members: 
    :synopsis: Define the plug-in architecture.
