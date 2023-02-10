.. _example.1d.ascan:

Example 1-D scan
++++++++++++++++

This SPEC data file (where for brevity of this example, additional content has
been removed) is a one-dimensional step scan of a counter named ``winCZT`` (last
column) versus a motor named ``Two Theta`` (first column) using a counting time
of 1 second per point. Data collection was configured to include data from an
additional counter named ``ic0``:

.. code-block::
   :linenos:

   #F /home/sricat/POLAR/data/CMR/lmn40.spe
   #E 918630612
   #D Wed Feb 10 01:10:12 1999
   #C spec1ID  User = polar
   #O0    Theta  Two Theta  sample x  sample y
   #o0 th tth samx samy

   #S 1  ascan  tth -0.7 -0.5  101 1
   #D Wed Feb 10 01:11:25 1999
   #T 1  (Seconds)
   #P0 -0.80000004 -0.60000003 -0.15875 0.16375
   #N 5
   #L Two Theta    Epoch  Seconds  ic0  winCZT
   -0.70000003  75 1 340592 1
   -0.69812503  76 1 340979 1
   -0.69612503  78 1 341782 1
   -0.69412503  79 1 342594 1
   -0.69212503  80 1 343300 0
   -0.69012503  82 1 341851 0
   -0.68812503  83 1 342126 1
   -0.68612503  85 1 342311 0
   -0.68425003  86 1 343396 1
   -0.68225003  88 1 343772 1
   -0.68025003  89 1 343721 1
   -0.67825003  91 1 341127 2
   -0.67625003  92 1 343733 0
   #C Wed Feb 10 01:12:39 1999.  More scan content removed for brevity.

The SPEC data file is written to a NeXus HDF5 file with this tree structure (for
brevity, additional structure has been removed):

.. code-block::
   :linenos:

   @default = "S1"
   S1:NXentry
     @default = "data"
     data:NXdata
       @axes = "Two_Theta"
       @signal = "winCZT"
       Epoch:NX_FLOAT64[13] = [75.0, 76.0, 78.0, '...', 92.0]
         @spec_name = "Epoch"
       Seconds:NX_FLOAT64[13] = [1.0, 1.0, 1.0, '...', 1.0]
         @spec_name = "Seconds"
       Two_Theta:NX_FLOAT64[13] = [-0.70000003, -0.69812503, -0.69612503, '...', -0.67625003]
         @spec_name = "Two Theta"
       ic0:NX_FLOAT64[13] = [340592.0, 340979.0, 341782.0, '...', 343733.0]
         @spec_name = "ic0"
       winCZT:NX_FLOAT64[13] = [1.0, 1.0, 1.0, '...', 0.0]
         @spec_name = "winCZT"
