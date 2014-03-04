spec2nexus
##########

Converts SPEC data files and scans into NeXus HDF5 files

:author:    Pete R. Jemian
:email:     prjemian@gmail.com
:copyright: 2014, Pete R. Jemian
:license:   Creative Commons Attribution 4.0 International Public License (see *LICENSE.txt*)
:URL:       http://prjemian.github.io/spec2nexus
:git:       https://github.com/prjemian/spec2nexus
:PyPI:      https://pypi.python.org/pypi/spec2nexus/ 
:Ohloh:     http://ohloh.net/p/spec2nexus

Provides
########

* **spec2nexus**  : command-line tool to convert SPEC data files to NeXus HDF5
* **prjPySpec**   : python binding to read SPEC [#]_ data files
* **eznx**        : (Easy NeXus) supports writing NeXus [#]_ HDF5 [#]_ files using h5py [#]_

.. [#] http://certif.com
.. [#] http://nexusformat.org
.. [#] http://hdfgroup.org
.. [#] http://h5py.org

Installation
############

Released versions of spec2nexus are available on `PyPI 
<https://pypi.python.org/pypi/spec2nexus/>`_. If you have the `Python Setup Tools 
<https://pypi.python.org/pypi/setuptools>`_ installed, then you can install 
using either::

    $ pip install spec2nexus

or:: 

    $ easy_install spec2nexus 

The latest development versions of spec2nexus can be downloaded from the
GitHub repository listed above::

    $ git clone http://github.com/prjemian/spec2nexus.git

To install in the standard Python location::

    $ cd spec2nexus
    $ python setup.py install

To install in user's home directory::

    $ python setup.py install --user

To install in an alternate location::

    $ python setup.py install --prefix=/path/to/installation/dir

Required Libraries
##################

========  =============================
Library   URL
========  =============================
h5py      http://www.h5py.org
numpy     http://numpy.scipy.org/
========  =============================

How to use spec2nexus
#####################

See the documentation (http://spec2nexus.github.io/spec2nexus) 
for complete instructions.

simple use
**********

Convert all scans in a SPEC data file::

    $ spec2nexus  path/to/file/specfile.dat

Writes ``path/to/file/specfile.hdf5`` (note: will not
overwrite if the HDF5 exists, use the *-f* option
to force overwrite).

show installed version
**********************

Verify the version of the installed spec2nexus::

   $ spec2nexus  -V
   2014.03.02

Help on usage
*************

::

   $ spec2nexus.py -h
   usage: spec2nexus [-h] [-e HDF5_EXTENSION] [-f] [-V] [-s SCAN_LIST] [-t]
                     [-q | -v]
                     infile [infile ...]
   
   spec2nexus: Convert SPEC data file into a NeXus HDF5 file.
   
   ...

..   
   positional arguments:
     infile                SPEC data file name(s)
   
   optional arguments:
     -h, --help            show this help message and exit
     -e HDF5_EXTENSION, --hdf5-extension HDF5_EXTENSION
                           NeXus HDF5 output file extension, default = .hdf5
     -f, --force-overwrite
                           overwrite output file if it exists
     -V, --version         show program's version number and exit
     -s SCAN_LIST, --scan SCAN_LIST
                           specify which scans to save, such as: -s all or -s 1
                           or -s 1,2,3-5 (no spaces!), default = all
     -q, --quiet           suppress all program output (except errors), do not
                           use with -v option
     -v, --verbose         print more program output, do not use with -q option
