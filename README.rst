
##########
spec2nexus
##########

Converts SPEC data files and scans into NeXus HDF5 files::

    $ spec2nexus  path/to/file/specfile.dat

Writes ``path/to/file/specfile.hdf5``

Provides
########

.. index:: SPEC, NeXus, HDF5, h5py

* **spec2nexus**       : command-line tool: Convert SPEC data files to NeXus HDF5
* **h5toText**         : command-line tool: Print the structure of an HDF5 file
* **extractSpecScan**  : command-line tool: Save columns from SPEC data file scan(s) to TSV files
* **spec**             : library: python binding to read SPEC [#]_ data files
* **eznx**             : library: (Easy NeXus) supports writing NeXus [#]_ HDF5 [#]_ files using h5py [#]_
* **specplot**         : command-line tool: plot a SPEC scan to an image file
* **specplot_gallery** : command-line tool: call **specplot** for all scans in a list of files, makes a web gallery

.. [#] http://certif.com
.. [#] http://nexusformat.org
.. [#] http://hdfgroup.org
.. [#] http://h5py.org

:author:    Pete R. Jemian
:email:     prjemian@gmail.com
:copyright: 2014-2017, Pete R. Jemian
:license:   Creative Commons Attribution 4.0 International Public License (see *LICENSE.txt*)
:URL:       documentation: http://spec2nexus.readthedocs.io
:git:       source: https://github.com/prjemian/spec2nexus
:PyPI:      Distribution: https://pypi.python.org/pypi/spec2nexus/ 
:OpenHub:   Compare open source software: https://www.openhub.net/p/spec2nexus
:Depsy:     Research software impact

    .. image:: http://depsy.org/api/package/pypi/spec2nexus/badge.svg
               :target: http://depsy.org/package/python/spec2nexus

:travis-ci: continuous integration

    .. image:: https://travis-ci.org/prjemian/spec2nexus.svg?branch=master
               :target: https://travis-ci.org/prjemian/spec2nexus

:coveralls: code coverage

   .. image:: https://coveralls.io/repos/github/prjemian/spec2nexus/badge.svg?branch=master
              :target: https://coveralls.io/github/prjemian/spec2nexus?branch=master
