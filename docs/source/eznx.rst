.. _eznx:

:mod:`spec2nexus.eznx`
######################

(Easy NeXus) support library for reading & writing NeXus HDF5 files using h5py

.. index:: examples; eznx

How to use :mod:`spec2nexus.eznx`
*********************************

Here is a simple example to write a NeXus data file using eznx:

.. literalinclude:: ../../spec2nexus/eznx_example.py
   :tab-width: 4
   :linenos:
   :language: guess


The output of this code is an HDF5 file (binary).
It has this structure:

.. code-block:: text
    :linenos:

	eznx_example.hdf5:NeXus data file
	  @default = entry
	  entry:NXentry
	    @NX_class = NXentry
	    @default = data
	    data:NXdata
	      @NX_class = NXdata
	      @signal = counts
	      @axes = two_theta
	      @two_theta_indices = 0
	      counts --> /entry/instrument/detector/counts
	      two_theta --> /entry/instrument/detector/two_theta
	    instrument:NXinstrument
	      @NX_class = NXinstrument
	      detector:NXdetector
	        @NX_class = NXdetector
	        counts:NX_FLOAT64[11] = __array
	          @units = counts
	          @target = /entry/instrument/detector/counts
	          __array = [1037.0, 2857.0, 23819.0, '...', 1321.0]
	        two_theta:NX_FLOAT64[11] = __array
	          @units = degrees
	          @target = /entry/instrument/detector/two_theta
	          __array = [17.926079999999999, 17.92558, 17.925080000000001, '...', 17.92108]

NeXus HDF5 File Structure
*************************

The output of this code is an HDF5 file (binary).
It has this general structure (indentation shows HDF5 groups, 
@ signs describe attributes of the preceding item):

.. code-block:: text
    :linenos:

      hdf5_file:NeXus data file
         @default = S1
         S1:NXentry     (one NXentry for each scan)
            @default = data
            title = #S
            T or M: #T or #M
            comments: #C for entire scan
            date: #D
            scan_number: #S
            G:NXcollection
               @description = SPEC geometry arrays, meanings defined by SPEC diffractometer support
               G0:NX_FLOAT64[] #G0
               G1:NX_FLOAT64[] #G1
               ...
            data:NXdata
               @description = SPEC scan data (content from #L and data lines)
               @signal = I0
               @axes = mr
               @mr_indices = 0
               Epoch:NX_FLOAT64[]
               I0:NX_FLOAT64[]         (last data column)
                 @spec_name = I0
               mr:NX_FLOAT64[]         (first data column)
               ...
            metadata:NXcollection
               @description = SPEC metadata (UNICAT-style #H & #V lines)
               ARenc_0:NX_FLOAT64 = 0.0
               ...
            positioners:NXcollection
               @description = SPEC positioners (#P & #O lines)
               mr:NX_FLOAT64
               ...



APIs provided:

.. toctree::
   :maxdepth: 1
   
   writer.rst

----

source code methods
*******************

.. autosummary::
   :nosignatures:

   ~spec2nexus.eznx.addAttributes
   ~spec2nexus.eznx.makeFile
   ~spec2nexus.eznx.makeDataset
   ~spec2nexus.eznx.makeExternalLink
   ~spec2nexus.eznx.makeGroup
   ~spec2nexus.eznx.openGroup
   ~spec2nexus.eznx.makeLink
   ~spec2nexus.eznx.read_nexus_field
   ~spec2nexus.eznx.read_nexus_group_fields
   ~spec2nexus.eznx.write_dataset

source code documentation
*************************

.. automodule:: spec2nexus.eznx
    :members: 
    :synopsis: (Easy NeXus) support reading & writing NeXus HDF5 files using h5py
    
