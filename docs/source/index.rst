
spec2nexus documentation
########################

Converts SPEC data files and scans into NeXus HDF5 files::

    $ spec2nexus  path/to/file/specfile.dat

Writes ``path/to/file/specfile.hdf5``

Provides
########

.. index:: SPEC, NeXus, HDF5, h5py

* :ref:`spec2nexus`        : command-line tool: Convert SPEC data files to NeXus HDF5
* :ref:`h5toText`          : command-line tool: Print the tree structure of an HDF5 file
* :ref:`extractSpecScan`   : command-line tool: Save columns from SPEC data file scan(s) to TSV files
* :ref:`pySpec`            : library: python binding to read SPEC [#]_ data files
* :ref:`prjPySpec`         : library: legacy version of **pySpec**, frozen at version 2014.0623.0
* :ref:`eznx`              : library: (Easy NeXus) supports writing NeXus [#]_ HDF5 [#]_ files using h5py [#]_

.. [#] http://certif.com
.. [#] http://nexusformat.org
.. [#] http://hdfgroup.org
.. [#] http://h5py.org


.. toctree::
   :maxdepth: 2
   :hidden:
   
   contents



This documentation built |today|. 
