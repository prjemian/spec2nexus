spec2nexus
##########

Converts SPEC data files and scans into NeXus HDF5 files

:version:   |version|
:release:   |release|
:published: |today|

:author:    Pete R. Jemian
:email:     prjemian@gmail.com
:copyright: 2014-2016, Pete R. Jemian
:license:   Creative Commons Attribution 4.0 International Public License (see *LICENSE.txt*)
:URL:       http://spec2nexus.readthedocs.io
:git:       https://github.com/prjemian/spec2nexus
:PyPI:      https://pypi.python.org/pypi/spec2nexus/ 
:Ohloh:     http://ohloh.net/p/spec2nexus

Provides
########

* **spec2nexus**      : command-line tool: Convert SPEC data files to NeXus HDF5
* **h5toText**        : command-line tool: Print the structure of an HDF5 file
* **extractSpecScan** : command-line tool: Save columns from SPEC data file scan(s) to TSV files
* **pySpec**          : library: python binding to read SPEC [#]_ data files
* **prjPySpec**       : library: legacy version of **pySpec**, frozen at version 2014.0623.0
* **eznx**            : library: (Easy NeXus) supports writing NeXus [#]_ HDF5 [#]_ files using h5py [#]_
* **specplot**        : command-line tool: plot a SPEC scan to an image file
* **specplot_gallery** : command-line tool: call **specplot** for all scans in a list of files, makes a web gallery

.. [#] http://certif.com
.. [#] http://nexusformat.org
.. [#] http://hdfgroup.org
.. [#] http://h5py.org
