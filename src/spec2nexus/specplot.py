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


def retrieve_specScanData(scan):
    '''retrieve default data from spec data file'''
    x = scan.data[scan.column_first]
    y = scan.data[scan.column_last]
    return (x, y)


def makeScanImage(scan, plotFile):
    '''
    make an image from the SPEC scan object
    
    :param obj scan: instance of :class:`~spec2nexus.spec.SpecDataFileScan`
    :param str plotFile: name of image file to write
    '''
    scanCmd = scan.scanCmd.split()[0]
    if scanCmd == 'some_custom_scan_macro':  # future feature
        # make simple image file of the data
        pass
    elif scanCmd in ('custom_scan', 'other_scan'):  # future feature
        # make simple image file of the data
        pass
    else:
        # plot last column v. first column
        plotData = retrieve_specScanData(scan)
        if len(plotData) > 0:
            # only proceed if mtime of SPEC data file is newer than plotFile
            mtime_sdf = os.path.getmtime(scan.header.parent.fileName)
            if os.path.exists(plotFile):
                mtime_pf = os.path.getmtime(plotFile)
            else:
                mtime_pf = 0
            if mtime_sdf > mtime_pf:
                # TODO: check if this scan _needs_ to be updated
                mpl__process_plotData(scan, plotData, plotFile)


def mpl__process_plotData(scan, plotData, plotFile):
    '''
    make MatPlotLib line chart image from raw SPEC or FlyScan data
    
    :param obj scan: instance of :class:`~spec2nexus.spec.SpecDataFileScan`
    :param obj plotData: tuple of x, y data: x & y are lists of numbers, same length
    :param str plotFile: name of image file to write
    '''
    x, y = plotData
    scan_macro = scan.scanCmd.split()[0]
    if scan_macro in ('some_custom_log_lin_scan'):  # future feature
        xlog = False
        ylog = True
        xtitle = scan.column_first
        ytitle = scan.column_last
    elif scan_macro in ('some_custom_log_log_scan', ):  # future feature
        xlog = True
        ylog = True
        xtitle = r'$|\vec{Q}|, 1/\AA$'
        ytitle = r'USAXS $R(|\vec{Q}|)$, a.u.'
    else:
        xlog = False
        ylog = False
        xtitle = scan.column_first
        ytitle = scan.column_last
    title = scan.specFile
    subtitle = "#%s: %s" % (scan.scanNum, scan.scanCmd)
    xy_plot(x, y,  plotFile, 
                       title=title,  subtitle=subtitle, 
                       xtitle=xtitle,  ytitle=ytitle, 
                       xlog=xlog, ylog=ylog,
                       timestamp_str=scan.date)


def openSpecFile(specFile):
    '''
    convenience routine so that others do not have to import spec2nexus.spec
    '''
    sd = spec.SpecDataFile(specFile)
    return sd


def findScan(sd, n):
    '''
    return the first scan with scan number "n"
    from the spec data file object or None
    '''
    scan = sd.getScan(str(n))
    return scan


def xy_plot(x, y, 
              plotfile, 
              title=None, subtitle=None, 
              xtitle=None, ytitle=None, 
              xlog=False, ylog=False,
              timestamp_str=None):
    '''
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

    .. tip:: use of this module as a background task
    
        MatPlotLib has several interfaces for plotting. 
        Since this module runs as part of a background job 
        generating lots of plots, the standard plt code is 
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
    parser = argparse.ArgumentParser(description=doc)
    parser.add_argument('specFile',    help="SPEC data file name")
    parser.add_argument('scan_number', help="scan number in SPEC file", type=str)
    parser.add_argument('plotFile',    help="output plot file name")
    results = parser.parse_args()

    specData = openSpecFile(results.specFile)
    scan = findScan(specData, results.scan_number)
    makeScanImage(scan, results.plotFile)


if __name__ == '__main__':
    main()


########### SVN repository information ###################
# $Date: 2016-06-06 16:32:15 -0500 (Mon, 06 Jun 2016) $
# $Author: jemian $
# $Revision: 1360 $
# $URL: https://subversion.xray.aps.anl.gov/small_angle/USAXS/livedata/specplot.py $
# $Id: specplot.py 1360 2016-06-06 21:32:15Z jemian $
########### SVN repository information ###################
