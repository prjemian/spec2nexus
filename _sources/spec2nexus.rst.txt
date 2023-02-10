.. _spec2nexus:

spec2nexus
##########

Converts SPEC data files and scans into NeXus HDF5 files.

.. index:: examples; spec2nexus

How to use **spec2nexus**
*************************

Convert all scans in a SPEC data file::

    $ spec2nexus  path/to/file/specfile.dat

Writes ``path/to/file/specfile.hdf5`` (Will not overwrite if the HDF5 exists,
use the ``-f`` option to force overwrite).

Describe the NeXus File
************************

The NeXus file could be simple or complex, depending on the data available in
the SPEC data file.  The content of the NeXus file is described in the following
sections.  See the :ref:`example.1d.ascan` section for an example.

.. toctree::
   :maxdepth: 2
   :glob:

   nexus_layout/index

show installed version
**********************

Verify the version of the installed spec2nexus::

   $ spec2nexus  -v
   2014.03.02

command-line options
********************

.. code-block:: text
    :linenos:

      user@host ~$ spec2nexus.py -h
      usage: spec2nexus [-h] [-e HDF5_EXTENSION] [-f] [-v] [-s SCAN_LIST]
                        [-o OUTPUT_FILENAME]
                        [--quiet | --verbose]
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
        -v, --version         show program's version number and exit
        -s SCAN_LIST, --scan SCAN_LIST
                              specify which scans to save, such as: -s all or -s 1
                              or -s 1,2,3-5 (no spaces!), default = all
        -o OUTPUT_FILENAME, --output OUTPUT_FILENAME
                              explicitly set the output file (default is same as input file, but with
                              the .spec extension changed to .hdf5)
        --quiet 	            suppress all program output (except errors), do not
                              use with --verbose option
        --verbose	            print more program output, do not use with --quiet
                              option


.. note:: Where's the source code to spec2nexus?

   In the source code, the *spec2nexus* program
   is started from file **nexus.py**
   (in the :meth:`spec2nexus.nexus.main`
   method, for those who look at the source code)::

      $ python nexus.py specfile.dat

   You're not really going to call that from the source directory, are you?
   It will work, *if* you have put that source directory on your PYTHONPATH.

----

source code documentation
*************************

.. automodule:: spec2nexus.nexus
    :members:
    :synopsis: Converts SPEC data files and scans into NeXus HDF5 files

