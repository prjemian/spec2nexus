.. _spec2nexus:

spec2nexus
##########

.. sidebar:: Where's the source to spec2nexus?

   In the source code, the *spec2nexus* program
   is started from file **cli.py** (in the :meth:`spec2nexus.cli.main`
   method, for those who look at the source code)::
   
      $ python cli.py specfile.dat

Converts SPEC data files and scans into NeXus HDF5 files.

command-line options
********************

::

   $ spec2nexus.py -h
   usage: spec2nexus [-h] [-e HDF5_EXTENSION] [-f] [-V] [-s SCAN_LIST] [-t]
                     [-q | -v]
                     infile [infile ...]
   
   spec2nexus: Convert SPEC data file into a NeXus HDF5 file.
   
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
     -t, --tree-only       print NeXus/HDF5 node tree (does not save to a file)
     -q, --quiet           suppress all program output (except errors), do not
                           use with -v option
     -v, --verbose         print more program output, do not use with -q option

.. index:: examples

How to use **spec2nexus**
*************************

Convert all scans in a SPEC data file::

    $ spec2nexus  path/to/file/specfile.dat

Writes ``path/to/file/specfile.hdf5`` (note: will not
overwrite if the HDF5 exists, use the *-f* option
to force overwrite).

----

source code documentation
*************************

.. automodule:: spec2nexus.cli
    :members: 
    :synopsis: Converts SPEC data files and scans into NeXus HDF5 files
    