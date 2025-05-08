
.. index:: plugin
.. index:: ! tree structure - NeXus HDF5

Basic Tree Structure
###########################

The basic tree structure of the NeXus HDF5 file is shown below:

.. code-block::
   :linenos:

    FILE_NAME:NXroot
        @default="S{SCAN_N}"
        S{SCAN_N}:NXentry
            @default="data"
            data:NXdata
                @axes={AXIS}
                @signal={SIGNAL}
                {AXIS}:NX_NUMBER[n] = ... data ...
                {SIGNAL}:NX_NUMBER[n] = ... data ...

.. sidebar:: ``NXroot``

   It is not required to write a ``NX_class="NXroot"`` [#NXroot]_ attribute to the
   root of any NeXus data file.  In fact, it is very rare to find this attribute
   in any NeXus HDF5 file.  We only show it here for guidance in how to build
   a file using the NeXus standard.

The root level of the file uses the structure of the NeXus **NXroot** [#NXroot]_
base class.

The ``@default`` attribute points the way to the default plottable data.
See the NeXus documentation [#NX.default]_ for more details.

.. note:: Here, the ``@`` character is used symbolically to identify this
   name is for an *attribute*.  Do not include the actual ``@`` symbol in
   the actual name of the attribute.

.. note:: ``AXIS`` and ``SIGNAL`` are the names of the first and last columns,
   respectively, of the scan and ``SCAN_N`` is the scan number from the scan's
   ``#S`` :index:`control line` [#spec.format]_ [#control_line]_ in the data file.

A NeXus **NXentry** [#NXentry]_ group (described symbolically as ``/SCAN``) will
be created for each scan to be written.  See section :ref:`data.file.scan` below
for more details.

.. sidebar:: image detectors

   SPEC data files do not usually contain data from a 2-D image
   detector.  A comment (or other control line such as ``#U``) may be used
   to describe the location of an external file containing such data
   and how to find the image frame from that file.  No standard
   pattern exists for SPEC data files to reference such images.

The scan data will be placed in a **NXdata** [#NXdata]_ group named ``data``
below the **NXentry** group.   See section :ref:`data.file.scan_data` below for
more details.

Other information from the scan will be written as described in the sections
below. There are variations on the tree structure as the complexity of a scan
increases. Examples of such variation include:

* multi-axis scans (such as ``a2scan``, ``a3scan``, ``a4scan``)
* multi-channel detectors
* 2-D and higher dimensionality scans (such as ``mesh``, ``hklmesh``, MCA)
* custom metadata
* comments

.. [#spec.format] SPEC **Standard Data-File Format** :   https://certif.com/spec_manual/mac_3_13.html
.. [#control_line] See :ref:`supplied_plugins` for a full list of the supported   control lines provided with **spec2nexus**.
.. [#NX.default] Used to identify the default plottable data in a NeXus HDF5 file.   https://manual.nexusformat.org/datarules.html#version-3

NeXus base classes

.. [#NXdata] **NXdata**:   https://manual.nexusformat.org/classes/base_classes/NXdata.html
.. [#NXentry] **NXentry**:   https://manual.nexusformat.org/classes/base_classes/NXentry.html
.. [#NXroot] **NXroot**:   https://manual.nexusformat.org/classes/base_classes/NXroot.html
