
spec2nexus documentation
########################

Converts SPEC data files and scans into NeXus HDF5 files::

    $ spec2nexus  path/to/file/specfile.dat

Writes ``path/to/file/specfile.hdf5``

Provides
########

.. index:: SPEC, NeXus, HDF5, h5py

* :ref:`spec2nexus`        : command-line tool to convert SPEC data files to NeXus HDF5
* :ref:`h5toText`          : command-line tool to print the tree structure of an HDF5 file
* :ref:`eznx`              : (Easy NeXus) supports writing NeXus [#]_ HDF5 [#]_ files using h5py [#]_
* :ref:`prjPySpec`         : python binding to read SPEC [#]_ data files
* :ref:`extractSpecScan`   : command-line tool to save columns from SPEC data file scan(s) to TSV files


.. [#] http://certif.com
.. [#] http://nexusformat.org
.. [#] http://hdfgroup.org
.. [#] http://h5py.org


.. toctree::
   :maxdepth: 2
   :hidden:
   
   contents



This documentation built |today|. 
