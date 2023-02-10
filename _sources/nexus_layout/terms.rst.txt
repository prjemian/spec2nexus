Nomenclature
###############

This page documents the terms used in the documentation of the NeXus files written
by **spec2nexus**.

==================  ==================  ==================
symbolic            example             meaning
==================  ==================  ==================
``NAME:NXclass``    ``data:NXdata``     HDF5 name of group and NeXus base class used
``{NAME}``          ``scan_number``     name is chosen as described
``@{NAME}``         ``@default``        HDF5 attribute of the parent group or field [#NX.field]_
``NX_{datatype}``   ``NX_NUMBER``       uses this NeXus data type [#NX.datatype]_
``NX_{unittype}``   ``NX_CHAR``         uses this NeXus unit type [#NX.unittype]_
``/SCAN``           ``/S1.1``           name of the scan **NXentry** [#NXentry] group in the NeXus HDF5 file
==================  ==================  ==================

.. note:: *for reference*: tree views

   In this documentation, the command [#punx]_::

       punx tree FILENAME.hdf5

   is used to generate a tree view of an HDF5 file's structure.

.. [#spec.format] SPEC **Standard Data-File Format** :
   https://certif.com/spec_manual/mac_3_13.html
.. [#NX.field] A NeXus **field** is the same as an HDF5 **dataset**.  The rename is
   due to historical reasons in NeXus when XML was used as a back-end data file
   storage format.
.. [#NX.datatype] List of NeXus data types:
   https://manual.nexusformat.org/nxdl-types.html#field-types-allowed-in-nxdl-specifications
.. [#NX.unittype] List of NeXus unit categories:
   https://manual.nexusformat.org/nxdl-types.html#unit-categories-allowed-in-nxdl-specifications
.. [#punx] Visualize NeXus file tree structure :
   https://prjemian.github.io/punx/tree.html#tree

NeXus base classes

.. [#NXbeam] **NXbeam**:   https://manual.nexusformat.org/classes/base_classes/NXbeam.html
.. [#NXdata] **NXdata**:   https://manual.nexusformat.org/classes/base_classes/NXdata.html
.. [#NXdetector] **NXdetector**:   https://manual.nexusformat.org/classes/base_classes/NXdetector.html
.. [#NXentry] **NXentry**:   https://manual.nexusformat.org/classes/base_classes/NXentry.html
.. [#NXinstrument] **NXinstrument**:   https://manual.nexusformat.org/classes/base_classes/NXinstrument.html
.. [#NXmonitor] **NXmonitor**: https://manual.nexusformat.org/classes/base_classes/NXmonitor.html
.. [#NXmonochromator] **NXmonochromator**:   https://manual.nexusformat.org/classes/base_classes/NXmonochromator.html
.. [#NXnote] **NXnote**:   https://manual.nexusformat.org/classes/base_classes/NXnote.html
.. [#NXpositioner] **NXpositioner**:   https://manual.nexusformat.org/classes/base_classes/NXpositioner.html
.. [#NXroot] **NXroot**:   https://manual.nexusformat.org/classes/base_classes/NXroot.html
.. [#NXsample] **NXsample**:   https://manual.nexusformat.org/classes/base_classes/NXsample.html
