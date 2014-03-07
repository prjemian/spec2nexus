.. _h5toText:

h5toText
########

Command line tool to print the structure of an HDF5 file


Example
*******

Here's an example from a test data file 
(**writer_1_3.h5** from the NeXus documentation):


.. code-block:: guess
    :linenos:

      [linux,512]$ h5toText -h data/writer_1_3.h5
      data/writer_1_3.h5 : NeXus data file
        Scan:NXentry
          @NX_class = NXentry
          data:NXdata
            @NX_class = NXdata
            counts:NX_INT32[31] = __array
              __array = [1037, 1318, 1704, '...', 1321]
              @units = counts
              @signal = 1
              @axes = two_theta
            two_theta:NX_FLOAT64[31] = __array
              __array = [17.926079999999999, 17.925909999999998, 17.925750000000001, '...', 17.92108]
              @units = degrees

usage
*****

the usage message::

   [linux,511]$ h5toText
   usage: h5toText [-h] [-n NUM_DISPLAYED] [-V] infile [infile ...]
   h5toText: error: too few arguments

the version number::

   [linux,511]$ h5toText -V
   2014.03.07

the help message::

   [linux,512]$ h5toText -h
   usage: h5toText [-h] [-n NUM_DISPLAYED] [-V] infile [infile ...]
   
   Print the structure of an HDF5 file
   
   positional arguments:
     infile            HDF5 data file name(s)
   
   optional arguments:
     -h, --help        show this help message and exit
     -n NUM_DISPLAYED  limit number of displayed array items to NUM_DISPLAYED
                       (must be 3 or more or 'None'), default = None
     -V, --version     show program's version number and exit


----

source code documentation
*************************

.. automodule:: spec2nexus.h5toText
    :members: 
    :synopsis: Command line tool to print the structure of an HDF5 file
    