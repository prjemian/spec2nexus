.. _specplot_gallery:

:mod:`spec2nexus.specplot_gallery`
##################################

Read a list of SPEC data files (or directory(s) containing SPEC data 
files) and plot images of all scans.  Store these images in subdirectories
of a given base directory (default: current directory) based on this structure::

   {base directory}
      /{year}
         /{month}
            /{spec file name}
                /index.html
                 s00001.png
                 s00002.png

The year and month are taken from the SPEC data file when the data were
collected.  The plot names include the scan numbers.  Here is an example::

   user@localhost $ specplot_gallery -d ./__demo__ ../src/spec2nexus/data/33bm_spec.dat 

.. figure:: img/gallery_screen_33bm.png
   :width: 95%
   
   Example of *specplot_gallery* showing scans from test file *33bm_spec.dat*.

Note that one of the scans could not be plotted.
Looking at the data file, it shows there is no data to plot::

   #C Wed Jun 16 19:00:10 2010.  Scan aborted after 0 points.

The last scan shown is from a *hklmesh* (2-D) scan.  It is mostly a 
constant background level, thus the large black area.

source code documentation
=========================

.. automodule:: spec2nexus.specplot_gallery
    :members: 
    :synopsis: Calls :mod:`spec2nexus.specplot` on a list of files or directories.  Makes a web gallery.
