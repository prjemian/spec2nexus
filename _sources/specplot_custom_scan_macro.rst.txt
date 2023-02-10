
.. _how_to_write_custom_scan_macro_handling:

How to write a custom scan handling class for *specplot*
#########################################################

Sometimes, it will be obvious that a certain scan macro never generates any plot
images, or that the default handling creates a plot that is a poor
representation of the data, such as the :ref:`hklscan <custom.hklscan.specplot>`
where only one of the the axes *hkl* is scanned.  To pick the scanned axis for
plotting, it is necessary to prepare custom handling and replace the default
handling.

Overview
********

It is possible to add in additional handling by writing a Python module.
This module creates a subclass of the standard handling, such as
:class:`~spec2nexus.specplot.LinePlotter`,
:class:`~spec2nexus.specplot.MeshPlotter`, or their superclass
:class:`~spec2nexus.specplot.ImageMaker`.
The support is added to the macro selection class
:class:`~spec2nexus.specplot.Selector` with code such as in the brief
example described below: :ref:`custom.ascan.specplot`::

    selector = spec2nexus.specplot.Selector()
    selector.add('ascan', Custom_Ascan)
    spec2nexus.specplot_gallery.main()


Data Model
**********

The data to be plotted is kept in an appropriate subclass of
:class:`~spec2nexus.converters.PlotDataStructure` in attributes show in the next
table.  The data model is an adaptation of the NeXus *NXdata* base class. [#]_

===============  =============================================================
attribute        description
===============  =============================================================
``self.signal``  name of the dependent data (*y* axis or image) to be plotted
``self.axes``    list of names of the independent axes [#]_
``self.data``    dictionary with the data, indexed by name (:math:`Q` & :math:`R`)
===============  =============================================================

.. [#] NeXus *NXdata* base class:
   https://download.nexusformat.org/doc/html/classes/base_classes/NXdata.html

.. [#] The number of names provided in `self.axes` is equal to the *rank*
   of the *signal* data (`self.data[self.signal]`).
   For 1-D data, `self.axes` has one name and the *signal* data is one-dimensional.
   For 2-D data, `self.axes` has two names and the *signal* data is two-dimensional.


Steps
*****

In all cases, custom handling of a specific SPEC macro name is provided by
creating a subclass of :class:`~spec2nexus.specplot.ImageMaker` and defining one
or more of its methods.  In the simplest case, certain settings may be changed
by calling :meth:`spec2nexus.specplot.ImageMaker.configure` with the custom
values.  Examples of further customization are provided below, such as when the
data to be plotted is stored outside of the SPEC data file.  This is common for
images from area detectors.

It may also be necessary to create a subclass of
:class:`~spec2nexus.converters.PlotDataStructure` to gather the data to be
plotted or override the default :meth:`spec2nexus.specplot.ImageMaker.plottable`
method. An example of this is shown with the
:class:`~spec2nexus.specplot.MeshPlotter` and associated
:class:`~spec2nexus.converters.MeshStructure` classes.


Examples
********

A few examples of custom macro handling are provided, some simple, some complex.
In each example, decisions have been made about where to provide the desired features.

.. _custom.ascan.specplot:

Change the plot title text in *ascan* macros
============================================

The SPEC *ascan* macro is a workhorse and records the scan of a positioner and
the measurement of data in a counter. Since this macro name ends with "scan",
the default selection in *specplot* images this data using the
:class:`~spec2nexus.specplot.LinePlotter` class. Here is a plot of the default
handling of data from the *ascan* macro:

.. figure:: img/ascan.png
   :width: 95%

   Standard plot of data from *ascan* macro

We will show how to change the plot title as a means to illustrate how to
customize the handling for a scan macro.

We write :class:`Custom_Ascan` which is a subclass of
:class:`~spec2nexus.specplot.LinePlotter`.  The :mod:`get_plot_data` method is
written (overrides the default method) to gain access to the place where we can
introduce the change.  The change is made by the call to the :mod:`configure`
method (defined in the superclass).  Here's the code:

.. rubric:: `ascan.py` example

.. literalinclude:: ../../demo/ascan.py
    :tab-width: 4
    :linenos:
    :language: python

See the changed title:

.. figure:: img/ascan_custom.png
   :width: 95%

   Customized plot of data from *ascan* macro


.. _custom.y_log.specplot:

Make the *y*-axis log scale
===========================

A very simple customization can make the Y axis to be logarithmic scale. (This
customization is planned for an added feature [#]_ in a future relase of the
*spec2nexus* package.)  We present two examples.

modify handling of `a2scan`
---------------------------

One user wants all the `a2scan` images to be plotted with a logarithmic
scale on the Y axis.  Here's the code:

.. rubric:: `custom_a2scan_gallery.py` example

.. literalinclude:: ../../demo/custom_a2scan_gallery.py
    :tab-width: 4
    :linenos:
    :language: python

custom `uascan`
---------------

The APS USAXS instrument uses a custom scan macro called *uascan* for routine
step scans. Since this macro name ends with "scan", the default selection in
*specplot* images this data using the :class:`~spec2nexus.specplot.LinePlotter`
class. Here is a plot of the default handling of data from the *uascan* macro:

.. figure:: img/uascan_as_ascan.png
   :width: 95%

   USAXS *uascan*, handled as :class:`~spec2nexus.specplot.LinePlotter`

The can be changed by making the *y* axis log scale. To do this, a custom
version of :class:`~spec2nexus.specplot.LinePlotter` is created as
:class:`Custom_Ascan`.  The :mod:`get_plot_data` method is written (overrides
the default method) to make the *y* axis log-scale by calling the
:mod:`configure` method (defined in the superclass).  Here's the code:

.. rubric:: `usaxs_uascan.py` example

.. literalinclude:: ../../demo/usaxs_uascan.py
    :tab-width: 4
    :linenos:
    :language: python

Note that in the *uascan*, a name for the sample provided by the user is given
in `self.scan.comments[0]`.  The plot title is changed to include this and the
scan number. The customized plot has a logarithmic *y* axis:

.. figure:: img/uascan_log_y.png
   :width: 95%

   USAXS *uascan*, with logarithmic *y* axis

The most informative view of this data is when the raw data are reduced to
:math:`I(Q)` and viewed on a log-log plot, but that process is beyond this
simple example. See the example :ref:`custom.usaxs.specplot` below.

.. [#] `specplot: add option for default log(signal)
        <https://github.com/prjemian/spec2nexus/issues/102>`_

.. _custom.hklscan.specplot:

SPEC's *hklscan* macro
======================

The SPEC *hklscan* macro appears in a SPEC data file due to either a *hscan*,
*kscan*, or *lscan*.  In each of these one of the *hkl* vectors is scanned while
the other two remain constant.

The normal handling of the *ascan* macro plots the last data column against the
first.  This works for data collected with the *hscan*. For *kscan* or *lscan*
macros, the *h* axis is still plotted by default since it is in the first
column.

.. figure:: img/hklscan_as_ascan.png
   :width: 95%

   SPEC *hklscan* (*lscan*, in this case), plotted against the (default) first axis *H*

To display the scanned axis, it is necessary to examine the data in a custom
subclass of :class:`~spec2nexus.specplot.LinePlotter`.  The
:class:`~spec2nexus.specplot.HKLScanPlotter` subclass, provided with *specplot*,
defines the :meth:`get_plot_data` method determines the scanned axis, setting it
by name::

      plot.axes = [axis,]
      self.scan.column_first = axis

Then, the standard plot handling used by *LinePlotter*
uses this information to make the plot.

.. figure:: img/hklscan.png
   :width: 95%

   SPEC *hklscan* (*lscan*), plotted against *L*

.. _custom.usaxs.specplot:

Get *xy* data from HDF5 file
============================

One example of complexity is when SPEC has been used to direct data collection
but the data is not stored in the SPEC data file.  The SPEC data file scan
must provide some indication about where the collected scan data has been stored.

custom `usaxs_flyscan`
------------------------------

The USAXS instrument at APS has a *FlyScan* macro that commands the instrument
to collect data continuously over the desired :math:`Q` range.  The data is written
to a NeXus HDF5 data file.  Later, a data reduction process converts the arrays of
raw data to one-dimensional :math:`I(Q)` profiles.  The best representation of this
reduced data is on a log-log plot to reveal the many decades of both :math:`I` and
:math:`Q` covered by the measurement.

With the default handling by :class:`~spec2nexus.specplot.LinePlotter`, no plot
can be generated since the data is given in a separate HDF5 file.  That file
is read with the custom handling of the `usaxs_flyscan.py` demo:

.. rubric:: `usaxs_flyscan.py` example

.. literalinclude:: ../../demo/usaxs_flyscan.py
    :tab-width: 4
    :linenos:
    :language: python

The data is then rendered in a customized log-log plot of :math:`I(Q)`:

.. figure:: img/usaxs_flyscan.png
   :width: 95%

   USAXS *FlyScan*, handled by :class:`USAXS_FlyScan_Plotter`

The ``USAXS_FlyScan_Plotter()`` class provides custom methods for
``retrieve_plot_data()`` and ``plottable()`` which will be called from
:meth:`spec2nexus.specplot.ImageMaker.plot_scan`.

Method ``USAXS_FlyScan_Plotter.plottable()`` returns a boolean value if the data
can be plotted.

Method ``USAXS_FlyScan_Plotter.retrieve_plot_data()`` gets the data from the
scan by calling ``retrieve_flyScanData()`` with the ``scan`` object.  Then the
method customizes the plot details.

Function ``retrieve_flyScanData(scan)`` gets the name of the NeXus/HDF5 file
from the scan and reads the HDF5 file, returning either the reduced data with
the number of points (as described in ``REDUCED_FLY_SCAN_BINS``) or the full
data set.

Usage
*****

When a custom scan macro handler is written and installed using code
similar to the :ref:`custom ascan <custom.ascan.specplot>` handling above::

   def main():
       selector = spec2nexus.specplot.Selector()
       selector.add('ascan', Custom_Ascan)
       spec2nexus.specplot_gallery.main()


   if __name__ == '__main__':
       main()

then the command line arugment handling from :meth:`spec2nexus.specplot_gallery.main`
can be accessed from the command line for help and usage information.

Usage::

   user@localhost ~/.../spec2nexus/demo $ ./ascan.py
   usage: ascan.py [-h] [-r] [-d DIR] paths [paths ...]
   ascan.py: error: too few arguments


Help::

   user@localhost ~/.../spec2nexus/demo $ ./ascan.py -h
   usage: ascan.py [-h] [-r] [-d DIR] paths [paths ...]

   read a list of SPEC data files (or directories) and plot images of all scans

   positional arguments:
     paths              SPEC data file name(s) or directory(s) with SPEC data
                        files

   optional arguments:
     -h, --help         show this help message and exit
     -r                 sort images from each data file in reverse chronolgical
                        order
     -d DIR, --dir DIR  base directory for output (default:/home/prjemian/Documen
                        ts/eclipse/spec2nexus/demo)

