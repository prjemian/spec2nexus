.. index:: ! plugin

:mod:`spec2nexus.plugin`
########################

An extensible plugin architecture is used to handle the different possible
:index:`!control line`
control lines (such as **#F**, **#E**, **#S**, ...) in a SPEC data file.

A SPEC *control line* provides metadata about the SPEC scan or SPEC data file.

Plugins can be used to parse or ignore certain control lines in SPEC data files.
Through this architecture, it is possible to support custom control lines, 
such as **#U** (SPEC standard control line for any user data).
One example is support for the :ref:`UNICAT-style <unicat_plugin>` of metadata 
provided in the scan header.

Plugins are now used to handle all control lines in :mod:`spec2nexus.spec`.
Any control line encountered but not recognized will be placed as text
in a NeXus **NXnote** group named ``unrecognized_NNN`` (where ``NNN``
is from 1 to the maximum number of unrecognized control lines).

.. _supplied_plugins:

Supplied **spec** plugin modules
********************************

These plugin modules are supplied:

.. autosummary::
   :nosignatures:
   
   ~spec2nexus.plugins.spec_common
   ~spec2nexus.plugins.fallback
   ~spec2nexus.plugins.apstools_specwriter
   ~spec2nexus.plugins.unicat
   ~spec2nexus.plugins.uim
   ~spec2nexus.plugins.uxml
   ~spec2nexus.plugins.XPCS
   
.. toctree::
   :maxdepth: 2
   :hidden:
   :glob:

   supplied_plugins/*

Writing a custom plugin
***********************

While **spec2nexus** provides a comprehensive set of plugins to handle the
common SPEC :index:`control line` control lines, custom control lines are used
at many facilities to write additional scan data and scan metadata into the SPEC
data file.  Custom plugins are written to process these additions.  See the
:ref:`how_to_write_plugin` section for details.

.. _control_line_table:

Overview of the supplied **spec** plugins
*****************************************

Plugins for these control lines [#]_ are provided in **spec2nexus**:

.. autosummary::
   :nosignatures:

   ~spec2nexus.plugins.spec_common.SPEC_File
   ~spec2nexus.plugins.spec_common.SPEC_Epoch
   ~spec2nexus.plugins.spec_common.SPEC_Date
   ~spec2nexus.plugins.spec_common.SPEC_Comment
   ~spec2nexus.plugins.spec_common.SPEC_Geometry
   ~spec2nexus.plugins.spec_common.SPEC_NormalizingFactor
   ~spec2nexus.plugins.spec_common.SPEC_CounterNames
   ~spec2nexus.plugins.spec_common.SPEC_CounterMnemonics
   ~spec2nexus.plugins.spec_common.SPEC_Labels
   ~spec2nexus.plugins.spec_common.SPEC_Monitor
   ~spec2nexus.plugins.spec_common.SPEC_NumColumns
   ~spec2nexus.plugins.spec_common.SPEC_PositionerNames
   ~spec2nexus.plugins.spec_common.SPEC_PositionerMnemonics
   ~spec2nexus.plugins.spec_common.SPEC_Positioners
   ~spec2nexus.plugins.spec_common.SPEC_HKL
   ~spec2nexus.plugins.spec_common.SPEC_Scan
   ~spec2nexus.plugins.spec_common.SPEC_CountTime
   ~spec2nexus.plugins.spec_common.SPEC_UserReserved
   ~spec2nexus.plugins.spec_common.SPEC_TemperatureSetPoint
   ~spec2nexus.plugins.spec_common.SPEC_DataLine
   ~spec2nexus.plugins.spec_common.SPEC_MCA
   ~spec2nexus.plugins.spec_common.SPEC_MCA_Array
   ~spec2nexus.plugins.spec_common.SPEC_MCA_Calibration
   ~spec2nexus.plugins.spec_common.SPEC_MCA_ChannelInformation
   ~spec2nexus.plugins.spec_common.SPEC_MCA_CountTime
   ~spec2nexus.plugins.spec_common.SPEC_MCA_RegionOfInterest
   ~spec2nexus.plugins.fallback.UnrecognizedControlLine
   ~spec2nexus.plugins.unicat.UNICAT_MetadataMnemonics
   ~spec2nexus.plugins.unicat.UNICAT_MetadataValues
   ~spec2nexus.plugins.uim.UIM_generic
   ~spec2nexus.plugins.XPCS.XPCS_VA
   ~spec2nexus.plugins.XPCS.XPCS_VD
   ~spec2nexus.plugins.XPCS.XPCS_VE

.. [#] Compare this list with :ref:`plugin_list`

source code documentation
*************************

.. automodule:: spec2nexus.plugin_core
    :members: 
    :synopsis: Define the plugin architecture.
