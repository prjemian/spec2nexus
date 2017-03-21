##########
spec2nexus
##########

Converts SPEC data files and scans into NeXus HDF5 files::

    $ spec2nexus  path/to/file/specfile.dat

Writes ``path/to/file/specfile.hdf5``

Provides
########

.. keywords - SPEC, NeXus, HDF5, h5py

* **spec2nexus**       : command-line tool: Convert `SPEC <http://certif.com>`_ data files to `NeXus <http://nexusformat.org>`_ `HDF5 <http://hdfgroup.org>`_
* **h5toText**         : command-line tool: Print the structure of an HDF5 file
* **extractSpecScan**  : command-line tool: Save columns from SPEC data file scan(s) to TSV files
* **spec**             : library: python binding to read SPEC data files
* **eznx**             : library: (Easy NeXus) supports writing NeXus HDF5 files using h5py
* **specplot**         : command-line tool: plot a SPEC scan to an image file
* **specplot_gallery** : command-line tool: call **specplot** for all scans in a list of files, makes a web gallery

Package Information
###################

* **author**:    Pete R. Jemian
* **email**:     prjemian@gmail.com
* **copyright**: 2014-2017, Pete R. Jemian
* **license**:   Creative Commons Attribution 4.0 International Public License (see `LICENSE.txt <http://spec2nexus.readthedocs.io/en/latest/license.html>`_ file)
* **URL**:       documentation: http://spec2nexus.readthedocs.io
* **git**:       source: https://github.com/prjemian/spec2nexus
* **PyPI**:      Distribution: https://pypi.python.org/pypi/spec2nexus/ 
* **OpenHub**:   Compare open source software: https://www.openhub.net/p/spec2nexus

..  see http://shields.io/ for more badge ideas

* **build badges**:
   .. image:: https://travis-ci.org/prjemian/spec2nexus.svg?branch=master
      :target: https://travis-ci.org/prjemian/spec2nexus
   .. image:: https://coveralls.io/repos/github/prjemian/spec2nexus/badge.svg?branch=master
      :target: https://coveralls.io/github/prjemian/spec2nexus?branch=master

* **release badges**:
   .. image:: https://img.shields.io/github/tag/prjemian/spec2nexus.svg
      :target: https://github.com/prjemian/spec2nexus/tags
   .. image:: https://img.shields.io/github/release/prjemian/spec2nexus.svg
      :target: https://github.com/prjemian/spec2nexus/releases
   .. image:: https://img.shields.io/pypi/v/spec2nexus.svg
      :target: https://pypi.python.org/pypi/spec2nexus/
   .. image:: https://anaconda.org/prjemian/spec2nexus/badges/version.svg
      :target: https://anaconda.org/prjemian/spec2nexus

* **community badges**
   .. image:: http://depsy.org/api/package/pypi/spec2nexus/badge.svg
      :target: http://depsy.org/package/python/spec2nexus
   .. image:: https://badges.gitter.im/spec2nexus/Lobby.svg
      :target: https://gitter.im/spec2nexus/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge
      :alt: Join the chat at https://gitter.im/spec2nexus/Lobby
