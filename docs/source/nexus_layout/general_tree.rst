General Tree Structure
----------------------

The **general tree structure** (with parts described in the sections below)
will follow this outline:

============================================= =============== =============================
HDF5 address                                  structure       reference
============================================= =============== =============================
``/``                                         (NXroot)        :ref:`data.file`
``/@default``                                 NX_CHAR         :ref:`data.file`
``/@SPEC_num_headers``                        NX_INT          :ref:`data.file`
``/SCAN``                                     NXentry         :ref:`data.file.scan`
``/SCAN/@default``                            NX_CHAR         :ref:`data.file.scan`
``/SCAN/command``                             NX_CHAR         :ref:`data.file.scan`
``/SCAN/comments``                            NX_CHAR         :ref:`data.file.scan`
``/SCAN/counter_cross_reference``             NXnote          :ref:`data.file.counters`
``/SCAN/counting_basis``                      NX_CHAR         :ref:`data.file.scan`
``/SCAN/data``                                NXdata          :ref:`data.file.scan_data`
``/SCAN/data/@axes``                          NX_CHAR         :ref:`data.file.scan_data`
``/SCAN/data/@signal``                        NX_CHAR         :ref:`data.file.scan_data`
``/SCAN/data/{AXIS}``                         NX_NUMBER       :ref:`data.file.scan_data`
``/SCAN/data/{COLUMN}``                       NX_NUMBER       :ref:`data.file.scan_data`
``/SCAN/data/{SIGNAL}``                       NX_NUMBER       :ref:`data.file.scan_data`
``/SCAN/date``                                NX_DATE_TIME    :ref:`data.file.scan`
``/SCAN/DEGC_SP``                             NX_NUMBER       :ref:`data.file.scan`
``/SCAN/experiment_description``              NX_CHAR         :ref:`data.file.scan`
``/SCAN/G``                                   NXnote          :ref:`data.file.geometry`
``/SCAN/G/G0``                                NX_NUMBER[]     :ref:`data.file.geometry`
``/SCAN/G/G1``                                NX_NUMBER[]     :ref:`data.file.geometry`
``/SCAN/G/G3``                                NX_NUMBER[]     :ref:`data.file.geometry`
``/SCAN/G/G4``                                NX_NUMBER[]     :ref:`data.file.geometry`
``/SCAN/instrument``                          NXinstrument    :ref:`data.file.instrument`
``/SCAN/instrument/diffractometer``           NXnote          :ref:`data.file.geometry`
``/SCAN/instrument/geometry_parameters``      NXnote          link to ``/SCAN/instrument/diffractometer``
``/SCAN/instrument/name``                     NX_CHAR         :ref:`data.file.geometry`
``/SCAN/instrument/monochromator``            NXmonochromator :ref:`data.file.geometry`
``/SCAN/instrument/monochromator/wavelength`` NX_NUMBER       :ref:`data.file.geometry`
``/SCAN/instrument/positioners``              NXnote          :ref:`data.file.positioners`
``/SCAN/M``                                   NX_NUMBER       :ref:`data.file.scan`
``/SCAN/MCA``                                 NXnote          :ref:`data.file.mca`
``/SCAN/metadata``                            NXnote          :ref:`data.file.metadata.HV`
``/SCAN/monitor``                             NXmonitor       :ref:`data.file.scan`
``/SCAN/monitor/preset``                      NX_NUMBER       :ref:`data.file.scan`
``/SCAN/positioner_cross_reference``          NXnote          :ref:`data.file.positioners`
``/SCAN/positioners``                         NXnote          :ref:`data.file.positioners`
``/SCAN/positioners/{POSITIONER}``            NXpositioner    :ref:`data.file.positioners`
``/SCAN/Q``                                   NX_NUMBER[3]    :ref:`data.file.geometry`
``/SCAN/sample``                              NXsample        :ref:`data.file.sample`
``/SCAN/sample/diffractometer_mode``          NX_CHAR         :ref:`data.file.geometry`
``/SCAN/sample/diffractometer_sector``        NX_NUMBER       :ref:`data.file.geometry`
``/SCAN/sample/ub_matrix``                    NX_NUMBER[3,3]  :ref:`data.file.geometry`
``/SCAN/sample/unit_cell_a``                  NX_NUMBER       only ``twoc`` geometry
``/SCAN/sample/unit_cell_abc``                NX_NUMBER[3]    :ref:`data.file.geometry`
``/SCAN/sample/unit_cell_alphabetagamma``     NX_NUMBER[3]    :ref:`data.file.geometry`
``/SCAN/sample/unit_cell_b``                  NX_NUMBER       only ``twoc`` geometry
``/SCAN/sample/unit_cell_gamma``              NX_NUMBER       only ``twoc`` geometry
``/SCAN/sample/unit_cell``                    NX_NUMBER[6]    :ref:`data.file.geometry`
``/SCAN/sample/beam``                         NXbeam          :ref:`data.file.geometry`
``/SCAN/sample/beam/incident_wavelength``     NX_NUMBER       :ref:`data.file.geometry`
``/SCAN/sample/or0``                          NXnote          :ref:`data.file.geometry`
``/SCAN/sample/or0/{ANGLE}``                  NX_NUMBER       :ref:`data.file.geometry`
``/SCAN/sample/or0/{HKL}``                    NX_NUMBER       :ref:`data.file.geometry`
``/SCAN/sample/or0/wavelength``               NX_NUMBER       :ref:`data.file.geometry`
``/SCAN/sample/or1``                          NXnote          :ref:`data.file.geometry`
``/SCAN/sample/or1/{ANGLE}``                  NX_NUMBER       :ref:`data.file.geometry`
``/SCAN/sample/or1/{HKL}``                    NX_NUMBER       :ref:`data.file.geometry`
``/SCAN/sample/or1/wavelength``               NX_NUMBER       :ref:`data.file.geometry`
``/SCAN/sample/temperature``                  NXlog           :ref:`data.file.temperature`
``/SCAN/scan_number``                         NX_INT          :ref:`data.file.scan`
``/SCAN/T``                                   NX_NUMBER       :ref:`data.file.scan`
``/SCAN/TEMP_SP``                             NX_NUMBER       :ref:`data.file.scan`
``/SCAN/title``                               NX_CHAR         :ref:`data.file.scan`
``/SCAN/{UNRECOGNIZED}``                      NXnote          :ref:`data.file.unrecognized`
``/SCAN/UserReserved``                        NXnote          :ref:`data.file.metadata.U`
``/SCAN/UXML``                                NXnote          :ref:`data.file.metadata.UXML`
============================================= =============== =============================


.. _nexus.base.classes:

NeXus base classes
++++++++++++++++++

These classes are used by **spec2nexus** to structure a NeXus HDF5 data file.

=================== =====================
NeXus base class    documentation URL
=================== =====================
NXbeam              https://manual.nexusformat.org/classes/base_classes/NXbeam.html
NXdata              https://manual.nexusformat.org/classes/base_classes/NXdata.html
NXdetector          https://manual.nexusformat.org/classes/base_classes/NXdetector.html
NXentry             https://manual.nexusformat.org/classes/base_classes/NXentry.html
NXinstrument        https://manual.nexusformat.org/classes/base_classes/NXinstrument.html
NXmonitor           https://manual.nexusformat.org/classes/base_classes/NXmonitor.html
NXmonochromator     https://manual.nexusformat.org/classes/base_classes/NXmonochromator.html
NXnote              https://manual.nexusformat.org/classes/base_classes/NXnote.html
NXpositioner        https://manual.nexusformat.org/classes/base_classes/NXpositioner.html
NXroot              https://manual.nexusformat.org/classes/base_classes/NXroot.html
NXsample            https://manual.nexusformat.org/classes/base_classes/NXsample.html
=================== =====================

Visit the NeXus documentation for a complete list of NeXus classes:
https://manual.nexusformat.org/classes/index.html

.. _nexus.data.types:

NeXus data types
++++++++++++++++++

These data types are used by **spec2nexus** to structure a NeXus HDF5 data file.

==============  ==============
type            description
==============  ==============
NX_CHAR         string representation (UTF-8)
NX_DATE_TIME    ISO8601 date/time representation
NX_INT          any representation of an integer number
NX_NUMBER       any valid NeXus number representation (scaler or array)
==============  ==============

Visit the NeXus documentation for a complete list of NeXus data types
(and unit categories): https://manual.nexusformat.org/nxdl-types.html
