NeXus File Layout
#################

.. https://github.com/prjemian/spec2nexus/issues/192

    from spec2nexus import spec, writer
    sdf = spec.SpecDataFile("one-scan.dat")
    scans = sdf.getScanNumbersChronological()
    writer.Writer(sdf).save("one-scan.hdf5", scan_list=scans)
    !punx tree one-scan.hdf5

SPEC data files contain data from one or more measurements called *scans*
written according to the **Standard Data-File Format**. [#spec.format]_  Each
scan is numbered (where the number is not necessarily unique within a data
file).  NeXus files are written [#]_ as HDF5 files with a tree structure [#]_
where the groups use the NeXus base class [#]_ definitions.

HDF5 files are binary (not human readable); in this documentation, the tree
structure (hierarchy) of the file will be shown.  Various terms are shown
symbolically, as described in the next table.

Contents

.. toctree::
   :maxdepth: 2
   :glob:

   example_1d_scan
   terms
   basic_tree
   general_tree
   spec_data_file
   spec_scan
   scan_data
   comments
   counters
   geometry
   instrument
   mca
   metadata
   positioners
   sample
   temperature
   unrecognized_content

.. [#spec.format] SPEC **Standard Data-File Format** :
   https://certif.com/spec_manual/mac_3_13.html
.. [#] NeXus objects and terms:
   https://manual.nexusformat.org/design.html#nexus-objects-and-terms
.. [#] NeXus tree structure:
   https://manual.nexusformat.org/introduction.html#example-of-a-nexus-file
.. [#] NeXus groups (base classes):
   https://manual.nexusformat.org/classes/base_classes/
