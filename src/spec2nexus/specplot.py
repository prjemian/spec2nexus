#!/usr/bin/env python

#-----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014-2017, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
#-----------------------------------------------------------------------------

'''
Plot the data from scan N in a SPEC data file

.. autosummary::

    ~Selector
    ~ImageMaker
    ~LinePlotter
    ~MeshPlotter
    ~NeXusPlotter
    ~xy_plot
    ~openSpecFile
    ~ScanAborted
    ~UnexpectedObjectTypeError

'''

import os
import datetime
import matplotlib
matplotlib.use('Agg')
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

import spec             # read SPEC data files
import singletons


class UnexpectedObjectTypeError(Exception): pass
# class UndefinedMacroNameError(Exception): pass
class ScanAborted(Exception): pass


class Selector(singletons.Singleton):
    '''
    associate SPEC scan macro names with image makers
    
    :image maker: subclass of :class:`ImageMaker`
    
    To include a custom image maker from outside this module,
    create the subclass and then add it to an instance of this
    class.  Such as this plotter that defaults to a logarithmic 
    scale for the X axis for all `logxscan` macros:
    
        from spec2nexus import specplot
        
        class LogX_Plotter(specplot.ImageMaker):

            def get_x_log(self):
                return True
        
        # ...
        
        selector = specplot.Selector()
        selector.add(`logxscan`, LogX_Plotter)
        
        # ...
        
        image_maker = specplot.Selector().auto(scan)
        plotter = image_maker()
        plotter.plot_scan(scan, fullPlotFile)

    This class is a singleton which means you will always get the same
    instance when you call this may times in your program.
    
    .. autosummary::
    
        ~auto
        ~add
        ~update
        ~get
        ~exists
        ~default

    '''
    default_key = '__default__'
    
    def __init__(self):
        self.db = {}
        self.add(self.default_key, LinePlotter, default=True)
    
    def auto(self, scan):
        '''
        automatically choose a scan image maker based on the SPEC scan macro
        
        Selection Rules:
        
        * macro ends with "scan": use :class:`LinePlotter`
        * macro ends with "mesh": use :class:`MeshPlotter`
        * default: use default image maker (initially :class:`LinePlotter`)
        '''
        if not isinstance(scan, spec.SpecDataFileScan):
            msg = 'expected a SPEC scan object, received: '
            msg += str(scan)
            raise UnexpectedObjectTypeError(msg)
        
        macro = scan.get_macro_name()
        if self.exists(macro):
            return self.get(macro)

        # adapt for different scan macros
        image_maker = self.default()
        if macro.lower().endswith('scan'):     
            image_maker = LinePlotter
        elif macro.lower().endswith('mesh'):
            image_maker = MeshPlotter

        # register this macro name
        self.add(macro, image_maker)
        return image_maker
    
    def add(self, key, value, default=False):
        '''
        register a new value by key
        
        :param str key: name of key, typically the macro name
        :raises KeyError: if key exists
        :raises UnexpectedObjectTypeError: if value is not subclass of :class:`ImageMaker`
        '''
        if self.exists(key):
            raise KeyError('key exists: ' + key)
        if not issubclass(value, ImageMaker):
            msg = 'expected subclass of ImageMaker, received type: '
            msg += type(value).__name__
            raise UnexpectedObjectTypeError(msg)

        self.db[key] = value
        if default:
            self.db[self.default_key] = value

        return value
    
    def update(self, key, value, default=False):
        '''
        replace an existing key with a new value
        
        :param str key: name of key, typically the macro name
        :raises KeyError: if key does not exist
        :raises UnexpectedObjectTypeError: if value is not subclass of :class:`ImageMaker`
        '''
        if not self.exists(key):
            raise KeyError('key does not exist: ' + key)
        if not issubclass(value, ImageMaker):
            msg = 'expected subclass of ImageMaker, received type: '
            msg += type(value).__name__
            raise UnexpectedObjectTypeError(msg)

        self.db[key] = value
        if default:
            self.db[self.default_key] = value

        return value
    
    def get(self, key):
        '''
        return a value by key
        
        :returns: subclass of :class:`ImageMaker` or `None` if key not found
        '''
        return self.db.get(key)
    
    def exists(self, key):
        '''
        is the key known? 
        '''
        return key in self.db
    
    def default(self):
        '''
        retrieve the value of the default key 
        '''
        return self.get(self.default_key)


class ImageMaker(object):
    '''
    superclass to handle plotting of data from a SPEC scan
    
    USAGE:
    
    #. Create a subclass of :class:`ImageMaker`
    #. Re-implement :meth:`make_image` to generate the plot image
    #. Re-implement :meth:`is_plottable` as appropriate for the available data
    #. In the call to :meth:`plot_scan`, supply any optional keywords to
       define plot settings such as `title`, `subtitle`, etc.
    #. Optionally, re-implement any of the various *get* methods to 
       further customize their behavior.
    
    EXAMPLE:

        class LinePlotter(ImageMaker):
            'create a line plot'
            
            def make_image(self, plotData, plotFile):
                """
                make MatPlotLib chart image from the SPEC scan
                
                :param obj plotData: object returned from :meth:`get_plot_data`
                :param str plotFile: name of image file to write
                """
                x, y = plotData
                xy_plot(x, y,  plotFile, 
                       title = self.get_plot_title(),
                       subtitle = self.get_plot_subtitle(),
                       xtitle = self.get_x_title(),
                       ytitle = self.get_y_title(),
                       xlog = self.get_x_log(),
                       ylog = self.get_y_log(),
                       timestamp_str = self.get_timestamp_str())

        sfile = specplot.openSpecFile(specFile)
        scan = sfile.getScan(scan_number)
        plotter = LinePlotter()
        plotter.plot_scan(scan, plotFile, y_log=True)
    
    TODO: describe how to override any of the settings in the dictionary
     
    Override any of these methods to customize the handling:
    
    .. TODO: convert this into an autosummary
     
    ========================== ==================================================
    method                     returns (as a string)
    ========================== ==================================================
    :meth:`get_data_file_name` the name of the file with the actual data
    :meth:`get_plot_data`      retrieve default data from spec data file
    :meth:`get_macro`          the name of the SPEC scan macro used
    :meth:`get_plot_title`     the name for the top of the plot
    :meth:`get_plot_subtitle`  optional smaller text below the title
    :meth:`get_x_title`        text for the independent (horizontal) axis
    :meth:`get_y_title`        text for the dependent (vertical) axis
    :meth:`get_x_log`          True: axis is logarithmic, False: axis is linear
    :meth:`get_y_log`          True: axis is logarithmic, False: axis is linear
    :meth:`get_timestamp_str`  text representing when the scan was recorded
    ========================== ==================================================

    .. autosummary::
    
        ~plot_scan
        ~make_image
        ~image
        ~get_initial_settings
        ~get_setting
        ~set_scan
        ~is_plottable
    
    '''

    def __init__(self):
        self.scan = None
        self.settings = self.get_initial_settings()
    
    def plot_scan(self, scan, plotFile, maker=None, **kwds):
        '''
        make an image plot of the data in the scan
        '''
        self.configure(**kwds)
        self.set_scan(scan)
        self.image(plotFile)
         
    def make_image(self, plotData, plotFile):
        '''
        make MatPlotLib chart image from the SPEC scan
        
        :param obj plotData: object returned from :meth:`get_plot_data`
        :param str plotFile: name of image file to write
        '''
        raise NotImplementedError('must implement make_image() in each subclass')
    
    def get_initial_settings(self):
        return dict(
            macro = None,
            title = None,
            subtitle = None,
            x_title = None,
            y_title = None,
            x_log = False,
            y_log = False,
            timestamp = None,
            xy_data = None,
        )
    
    def get_setting(self, key):
        return self.settings.get(key)
    
    def _verify_setting_name_(self, key):
        if key not in self.settings:
            raise KeyError('unknown plot option: ' + key)
    
    def configure(self, **kwds):
        '''
        set any of the plot options
        '''
        for k, v in kwds.items():
            self._verify_setting_name_(k)
            self.settings[k] = v

    def set_scan(self, scan):
        '''
        assign the SPEC scan object
         
        :param obj scan: instance of :class:`~spec2nexus.spec.SpecDataFileScan`
        '''
        if not isinstance(scan, spec.SpecDataFileScan):
            raise UnexpectedObjectTypeError('scan object not a SpecDataFileScan')
        self.scan = scan
     
    def is_plottable(self, plotData):
        '''
        is there enough data to make a plot?
        '''
        return plotData is not None     # subclass should provide a deeper test
         
    def image(self, plotFile):
        '''
        make an image, if permissable, from data in (or referenced by) the SPEC scan object
         
        :param str plotFile: name of image file to write
        '''
        try:
            plotData = self.get_plot_data()
        except KeyError, _exc:
            was_aborted = self.scan.__getattribute__('_aborted_')
            if was_aborted is not None:
                raise ScanAborted(was_aborted)
            raise _exc
        if self.is_plottable(plotData):
            # only proceed if mtime of SPEC data file is newer than plotFile
            mtime_sdf = os.path.getmtime(self.get_data_file_name())
            if os.path.exists(plotFile):
                mtime_pf = os.path.getmtime(plotFile)
            else:
                mtime_pf = 0
            if mtime_sdf > mtime_pf:
                self.make_image(plotData, plotFile)

    def get_data_file_name(self):
        '''
        the name of the file with the actual data
        
        Usually, this is the SPEC data file
        but it *could* be something else
        '''
        return self.scan.header.parent.fileName
    
    def get_plot_data(self):
        '''retrieve default data from spec data file'''
        if self.get_setting('xy_data') is not None:
            return self.get_setting('xy_data')

        # plot last column v. first column
        x = self.scan.data[self.scan.column_first]
        y = self.scan.data[self.scan.column_last]
        return (x, y)
    
    def get_macro(self):
        'return the name of the SPEC macro for this scan'
        return self.scan.get_macro_name()
    
    def get_plot_title(self):
        'return the plot title, default is the name of the SPEC data file'
        return self.get_setting('title') or self.scan.specFile
    
    def get_plot_subtitle(self):
        'return the subtitle, default includes scan number and command'
        return self.get_setting('subtitle') or '#' + str(self.scan.scanNum) + ': ' + self.scan.scanCmd
    
    def get_x_title(self):
        'return the title for the X axis, default is label of first column in the scan'
        return self.get_setting('x_title') or self.scan.column_first
    
    def get_y_title(self):
        'return the title for the Y axis, default is label of last column in the scan'
        return self.get_setting('y_title') or self.scan.column_last
    
    def get_x_log(self):
        'boolean: should the X axis be plotted on a log scale?'
        return self.get_setting('x_log')
    
    def get_y_log(self):
        'boolean: should the Y axis be plotted on a log scale?'
        return self.get_setting('y_log')
    
    def get_timestamp_str(self):
        'return the time of this scan as a string, default is date/time from the SPEC scan'
        return self.get_setting('timestamp') or self.scan.date


class LinePlotter(ImageMaker):
    '''
    create a line plot
    '''
    
    def make_image(self, plotData, plotFile):
        '''
        make MatPlotLib chart image from the SPEC scan
        
        :param obj plotData: object returned from :meth:`get_plot_data`
        :param str plotFile: name of image file to write
        '''
        x, y = plotData
        xy_plot(x, y,  plotFile, 
               title = self.get_plot_title(),
               subtitle = self.get_plot_subtitle(),
               xtitle = self.get_x_title(),
               ytitle = self.get_y_title(),
               xlog = self.get_x_log(),
               ylog = self.get_y_log(),
               timestamp_str = self.get_timestamp_str())


class MeshPlotter(ImageMaker):
    '''
    create a mesh plot (2-D image)
    '''
    # see code in: writer.Writer.mesh()
    
    def get_plot_data(self):
        '''retrieve default data from spec data file'''
        raise NotImplementedError(self.__class__.__name__ + '() is not ready')
        if self.get_setting('xy_data') is not None:
            return self.get_setting('xy_data')
    
    def make_image(self, plotData, plotFile):
        '''
        make MatPlotLib chart image from the SPEC scan
        
        :param obj plotData: object returned from :meth:`get_plot_data`
        :param str plotFile: name of image file to write
        '''
        raise NotImplementedError(self.__class__.__name__ + '() is not ready')


class NeXusPlotter(ImageMaker):
    '''
    create a plot from a NeXus HDF5 data file
    '''
    
    def make_image(self, plotData, plotFile):
        '''
        make image file from the SPEC scan
        
        :param obj plotData: object returned from :meth:`get_plot_data`
        :param str plotFile: name of image file to write
        '''
        raise NotImplementedError(self.__class__.__name__ + '() is not ready')


def xy_plot(x, y, 
              plotfile, 
              title=None, subtitle=None, 
              xtitle=None, ytitle=None, 
              xlog=False, ylog=False,
              timestamp_str=None):
    r'''
    with MatPlotLib, generate a plot of a scan (as if data from a scan in a SPEC file)
    
    :param [float] x: horizontal axis data
    :param [float] y: vertical axis data
    :param str plotfile: file name to write plot image
    :param str xtitle: horizontal axis label (default: not shown)
    :param str ytitle: vertical axis label (default: not shown)
    :param str title: title for plot (default: date time)
    :param str subtitle: subtitle for plot (default: not shown)
    :param bool xlog: should X axis be log (default: False=linear)
    :param bool ylog: should Y axis be log (default: False=linear)
    :param str timestamp_str: date to use on plot (default: now)

    .. tip:: use this module as a background task
    
        MatPlotLib has several interfaces for plotting. 
        Since this module runs as part of a background job 
        generating lots of plots, MatPlotLib's standard ``plt`` code is 
        not the right model.  It warns after 20 plots and 
        will eventually run out of memory.  
        
        Here's the fix used in this module:
        http://stackoverflow.com/questions/16334588/create-a-figure-that-is-reference-counted/16337909#16337909

    '''
    fig = matplotlib.figure.Figure(figsize=(9, 5))
    fig.clf()

    ax = fig.add_subplot('111')
    if xlog:
        ax.set_xscale('log')
        if max(x) <= 0:
            msg = 'X data has no positive values,'
            msg += ' and therefore can not be log-scaled.'
            raise ValueError(msg)
    if ylog:
        ax.set_yscale('log')
        if max(y) <= 0:
            msg = 'Y data has no positive values,'
            msg += ' and therefore can not be log-scaled.'
            raise ValueError(msg)
    if not xlog and not ylog:
        ax.ticklabel_format(useOffset=False)
    if xtitle is not None:
        ax.set_xlabel(xtitle)
    if ytitle is not None:
        ax.set_ylabel(ytitle)

    if subtitle is not None:
        ax.set_title(subtitle, fontsize=9)

    if timestamp_str is None:
        timestamp_str = str(datetime.datetime.now())
    if title is None:
        title = timestamp_str
    else:
        fig.text(0.02, 0., timestamp_str,
            fontsize=8, color='gray',
            ha='left', va='bottom', alpha=0.5)
    fig.suptitle(title, fontsize=10)

    ax.plot(x, y, 'o-')

    FigureCanvas(fig).print_figure(plotfile, bbox_inches='tight')


def openSpecFile(specFile):
    '''
    convenience routine so that others do not have to import spec2nexus.spec
    '''
    sd = spec.SpecDataFile(specFile)
    return sd


def main():
    import argparse
    doc = __doc__.strip().splitlines()[0]
    p = argparse.ArgumentParser(description=doc)
    p.add_argument('specFile',    help="SPEC data file name")
    p.add_argument('scan_number', help="scan number in SPEC file", type=str)
    p.add_argument('plotFile',    help="output plot file name")
    args = p.parse_args()
    
    sfile = openSpecFile(args.specFile)
    scan = sfile.getScan(args.scan_number)
    image_maker = Selector().auto(scan)
    plotter = image_maker()
    plotter.plot_scan(scan, args.plotFile)


if __name__ == '__main__':
    main()
