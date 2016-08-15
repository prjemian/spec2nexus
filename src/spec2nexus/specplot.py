#!/usr/bin/env python

'''
read a SPEC data file and plot scan n
'''

import os
import datetime
import matplotlib
matplotlib.use('Agg')
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

import spec             # read SPEC data files


__registry__ = None


class UnexpectedObjectTypeError(Exception): pass
class UndefinedMacroNameError(Exception): pass


class Registry(object):
    '''
    register all the plot handlers
    '''
    
    def __init__(self):
        global __registry__
        if __registry__ is None:    # singleton
            __registry__ = {}
        self.db = __registry__
    
    def add(self, value):
        if not isinstance(value, MacroPlotHandler):
            msg = 'handler not a subclass of MacroPlotHandler'
            raise UnexpectedObjectTypeError(msg)
        if value.macro is None:
            msg = 'subclass must define a str value for *macro*'
            raise UndefinedMacroNameError(msg)
        self.db[value.macro] = value
    
    def exists(self, key):
        return key in self.db
    
    def get(self, key):
        if not self.exists(key):
            raise KeyError('not found: ' + key)
        return self.db[key]


class MacroPlotHandler(object):
    '''
    superclass to handle plotting of data collected using a specific SPEC macro
    
    The *macro* key (``self.macro``) must be set to the *exact* name
    of the SPEC scan macro as recorded in the data file.  The *macro* key
    must be unique amongst all instances of :class:`MacroPlotHandler`
    so the software can pick the correct instance for plotting.
    
    Override any of these methods to customize the handling:
    
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
    '''
    
    macro = None    # must define in subclass
    
    def __init__(self):
        self.scan = None
    
    def set_scan(self, scan):
        '''
        assign the SPEC scan object
        
        :param obj scan: instance of :class:`~spec2nexus.spec.SpecDataFileScan`
        '''
        if isinstance(scan, spec.SpecDataFileScan):
            raise UnexpectedObjectTypeError('scan object not a SpecDataFileScan')
        self.scan = scan
    
    def is_plottable(self, plotData):
        '''
        is there enough data to make a plot?
        '''
        return self.get_macro() == self.macro and len(plotData) > 0
        
    def image(self, plotFile):
        '''
        make an image, if permissable, from the SPEC scan object
        
        :param str plotFile: name of image file to write
        '''
        plotData = self.get_plot_data()
        if self.is_plottable(plotData):
            # only proceed if mtime of SPEC data file is newer than plotFile
            mtime_sdf = os.path.getmtime(self.get_data_file_name())
            if os.path.exists(plotFile):
                mtime_pf = os.path.getmtime(plotFile)
            else:
                mtime_pf = 0
            if mtime_sdf > mtime_pf:
                self.make_image(plotData, plotFile)
        
    def make_image(self, plotData, plotFile):
        '''
        make MatPlotLib chart image from the SPEC scan
        
        :param obj plotData: object returned from :meth:`get_plot_data`
        :param str plotFile: name of image file to write
        '''
        x, y = plotData
        xy_plot(x, y,  plotFile, 
               title=self.get_plot_title(),
               subtitle=self.get_plot_subtitle(),
               xtitle=self.get_x_title(),
               ytitle=self.get_y_title(),
               xlog=self.get_x_log(),
               ylog=self.get_y_log(),
               timestamp_str=self.get_timestamp_str())
    
    def get_data_file_name(self):
        '''
        the name of the file with the actual data
        
        Usually, this is the SPEC data file
        but it *could* be something else
        '''
        return self.scan.header.parent.fileName
    
    def get_plot_data(self):
        '''retrieve default data from spec data file'''
        # plot last column v. first column
        x = self.scan.data[self.scan.column_first]
        y = self.scan.data[self.scan.column_last]
        return (x, y)
    
    def get_macro(self):
        ' '
        return self.scan.get_macro_name()
    
    def get_plot_title(self):
        ' '
        return self.scan.specFile
    
    def get_plot_subtitle(self):
        ' '
        return '#' + str(self.scan.scanNum) + ': ' + self.scan.scanCmd
    
    def get_x_title(self):
        ' '
        return self.scan.column_first
    
    def get_y_title(self):
        ' '
        return self.scan.column_last
    
    def get_x_log(self):
        ' '
        return False
    
    def get_y_log(self):
        ' '
        return False
    
    def get_timestamp_str(self):
        ' '
        return self.scan.date


class Plotter(object):
    '''
    '''
    
    def __init__(self):
        self.registry = self.register_handlers()
    
    def plot_scan(self, scan, plotFile):
        '''
        '''
        macro = scan.get_macro_name()
        if not self.registry.exists(macro):
            # raise UndefinedMacroNameError(macro)
            # try a little harder: if no handler exists, try the default one anyway
            self.registry.add(Macro_1D_Scan_HandlerFactory(macro))

        handler = self.registry.get(macro)
        handler.set_scan(scan)
        handler.image(plotFile)

    def register_handlers(self):
        '''
        subclass Plotter() and override this method to add more handlers
        '''
        registry = Registry()
        # this will happen by default, it's a demo of the default handling
        # ascan = Macro_1D_Scan_HandlerFactory('ascan')
        # registry.add(ascan)
        return registry


class Macro_1D_Scan_HandlerFactory(MacroPlotHandler):
    '''
    creates an instance of :class:`MacroPlotHandler` with a defined macro name
    
    Use this convenience class to simplify the support of many common
    SPEC scan macros that result in a 1-D scan where the plot should
    be generated from the last column *v.* the first column.
    
    .. rubric:: Usage
    
    ::
    
        ascan = Macro_1D_Scan_HandlerFactory('ascan')
    
    To support a 2-D (or higher) scan, such as a mesh or image, make
    a subclass of :class:`MacroPlotHandler` and override the appropriate
    methods.
    '''
    
    def __init__(self, macro):
        MacroPlotHandler.__init__(self)
        self.macro = macro

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def openSpecFile(specFile):
    '''
    convenience routine so that others do not have to import spec2nexus.spec
    '''
    sd = spec.SpecDataFile(specFile)
    return sd


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
    if ylog:
        ax.set_yscale('log')
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
    plotter = Plotter()
    plotter.plot_scan(scan, args.plotFile)


if __name__ == '__main__':
    import sys
    if not os.path.exists('__plots__'):
        os.mkdir('__plots__')
    s = 'data/02_03_setup.dat 1 __plots__/image.png'
    for item in s.split():
        sys.argv.append(item)
    main()
