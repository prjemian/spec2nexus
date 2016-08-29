#!/usr/bin/env python

'''
read a list of SPEC data file and plot images of all scans

The images are stored in files in a directory structure
that is organized chronologically,
such as: ``yyyy/mm/spec_file/s1.png``.
The root of the directory is either specified by the 
command line ``-d`` option or  defaults to the current 
working directory.  The ``yyyy/mm`` (year and month) are 
taken from the ``#D`` line of the SPEC data file.
The ``spec_file`` is the file name with file extension 
and directory name removed.  The image file names are
derived from the scan numbers.
'''


import datetime
import logging
import os
import shutil
import sys

import spec
import specplot


MTIME_CACHE_FILE = 'mtime_cache.txt'


class DirectoryNotFoundError(ValueError): pass


class PlotSpecFileScans(object):
    '''
    read a SPEC data file and plot thumbnail images of all its scans
    
    :param [str] filelist: list of SPEC data files to be checked
    :param str plotDir: name of base directory to store output image thumbnails
    '''

    def __init__(self, filelist, plotDir = None):
        self.filelist = filelist
        self.plotDir = plotDir or os.getcwd()
        self.plotter = specplot.Plotter()

        for specFile in filelist:
            self.plot_all_scans(specFile)
    
    def _mtime_checkup_(self, specFile):
        '''
        check the mtime of various files to see if the plot needs to be made
        '''
        if not os.path.exists(specFile):
            return
    
        # decide here if SPEC file needs to be opened for possible replot of scan data
        mtime_cache = Cache_File_Mtime(self.plotDir)
        if not mtime_cache.was_file_updated(specFile):
            return
    
        # Don't replot if the plot newer than the data file modification time.
        mtime_specFile = mtime_cache.get(specFile)
        png_directory = self.get_PngDir(specFile)
        if os.path.exists(png_directory):
            mtime_pngdir = get_file_mtime(png_directory)
        else:
            mtime_pngdir = 0
    
        # compare mtime of data file with mtime of PNG directory
        if mtime_pngdir > mtime_specFile:
            # do nothing if plot directory was last updated _after_ the specFile
            return
        
        return (mtime_specFile, mtime_cache, mtime_pngdir, png_directory)
    
    def plot_all_scans(self, specFile):
        '''
        plot all the recognized scans from the file named ``specFile``
        '''
        if not spec.is_spec_file(specFile):
            return

        answer = self._mtime_checkup_(specFile)
        if answer is None:
            return
        mtime_specFile, mtime_cache, mtime_pngdir, png_directory = answer

        try:
            logger('SPEC data file: ' + specFile)
            logger('  updating plots in directory: ' + png_directory)
            logger('    mtime_specFile: ' + str(mtime_specFile))
            logger('    mtime_pngdir:   ' + str(mtime_pngdir))
            sd = specplot.openSpecFile(specFile)
        except:
            return    # could not open file, be silent about it
        if len(sd.headers) == 0:    # no scan header found, again, silence
            return
    
        plotList = []
        newFileList = [] # list of all new files created
    
        if not os.path.exists(png_directory):
            os.makedirs(png_directory)
            logger('creating directory: ' + png_directory)
        
        shutil.copy(specFile, png_directory)
    
        for scan_number in sd.getScanNumbers():
            # TODO: was the data in _this_ scan changed since the last time the SPEC file was modified?
            #  Check the scan's date/time stamp and also if the plot exists.
            #  For a scan N, the plot may exist if the scan was in progress at the last update.
            #  For sure, if a plot for N+1 exists, no need to remake plot for scan N.  Thus:
            #    Always remake if plot for scan N+1 does not exist
            scan = sd.getScan(scan_number)
            basePlotFile = 's' + str(scan.scanNum) + '.png'
            fullPlotFile = os.path.join(png_directory, basePlotFile)
            altText = '#' + str(scan.scanNum) + ': ' + scan.scanCmd
            href = self.href_format(basePlotFile, altText)
            plotList.append(href)
            #print "specplot.py %s %s %s" % (specFile, scan.scanNum, fullPlotFile)
            if needToMakePlot(fullPlotFile, mtime_specFile):
                try:
                    logger('  creating SPEC data scan image: ' + basePlotFile)
                    self.plotter.plot_scan(scan, fullPlotFile)
                    newFileList.append(fullPlotFile)
                except:
                    exc = sys.exc_info()[1]
                    msg = "ERROR: '%s' %s #%s" % (exc, specFile, scan.scanNum)
                    # print msg
                    plotList.pop()     # rewrite the default link
                    plotList.append("<!-- " + msg + " -->")
                    altText = str(exc) + ': ' + str(scan.scanNum) + ' ' + scan.scanCmd
                    href = self.href_format(basePlotFile, altText)
                    plotList.append(href)
    
        htmlFile = os.path.join(png_directory, "index.html")
        if len(newFileList) or not os.path.exists(htmlFile):
            logger('  creating/updating index.html file')
            html = build_index_html(specFile, plotList)
            f = open(htmlFile, "w")
            f.write(html)
            f.close()
            newFileList.append(htmlFile)
            
        # touch to update the mtime on the png_directory
        os.utime(png_directory, None)
    
    def get_PngDir(self, specFile):
        '''
        return the PNG directory based on the specFile
        
        :param str specFile: name of SPEC data file (relative or absolute)
        '''
        data_file_root_name = os.path.splitext(os.path.split(specFile)[1])[0]
        date_str = get_SpecFileDate(specFile)
        if date_str is None:
            return
        return self.getBaseDir(data_file_root_name, date_str)

    def getBaseDir(self, basename, date):
        '''
        find the path based on the date in the spec file
        '''
        return os.path.join(self.plotDir, datePath(date), basename)
    
    def href_format(self, basePlotFile, altText):
        href = '<a href="' + basePlotFile + '">'
        href += '<img src="' + basePlotFile + '"'
        href += ' width="150" height="75"'
        href += ' alt="' + altText + '"/>'
        href += '</a>'
        return href


class Cache_File_Mtime(object):
    '''
    maintain a list of all known data file modification times
    
    :param str base_dir: name of base directory to store output image thumbnails
    
    This list will allow the code to avoid unnecessary work
    reparsing and plotting of unchanged SPEC data files.
    '''

    def __init__(self, base_dir):
        if not os.path.exists(base_dir):
            msg = 'directory does not exist: ' + base_dir
            raise DirectoryNotFoundError(msg)
        self.base_dir = os.path.abspath(base_dir)
        self.cache_file = os.path.join(self.base_dir, MTIME_CACHE_FILE)
        self.cache = self.read()

    def read(self):
        '''read the cache from storage'''
        cache = {}
        if os.path.exists(self.cache_file):
            for line in open(self.cache_file, 'r').readlines():
                key = line.split('\t')[0]
                val = float(line.strip().split('\t')[1])
                cache[key] = val
        return cache

    def write(self):
        '''write the cache to storage'''
        f = open(self.cache_file, 'w')
        for key, val in sorted(self.cache.items()):
            t = str(key) + '\t' + str(val) + '\n'
            f.write(t)
        f.close()
    
    def get(self, fname):
        '''
        get the file modified time from the cache
        
        :param str fname: file name, already known to exist
        :return: time (float) cached value of when fname was 
            last modified or None if not known
        '''
        if fname in self.cache:
            return self.cache[fname]
        return None

    def was_file_updated(self, fname):
        '''
        compare the mtime between disk and cache
        
        :param str fname: file name, already known to exist
        :return bool: True if file is newer than the cache (or new to the cache)
        '''
        mtime_file = get_file_mtime(fname)
        mtime_cache = self.get(fname)
        if mtime_cache is None or mtime_file > mtime_cache:
            logger('SPEC data file updated: ' + fname)
            self.cache[fname] = mtime_file
            self.write()
            return True
        return False

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def datePath(date):
    '''
    convert the date into a path: yyyy/mm
    
    :param str date: text date from SPEC file #D line: 'Thu Jun 19 12:21:55 2014'
    '''
    import time
    dateStr = time.strptime(date, "%a %b %d %H:%M:%S %Y")
    yyyy = "%04d" % dateStr.tm_year
    mm = "%02d" % dateStr.tm_mon
    return os.path.join(yyyy, mm)


def get_SpecFileDate(specFile):
    '''
    return the #D date of the SPEC data file or None
    
    :param str specFile: name of SPEC data file (relative or absolute)
    '''
    # Get that without parsing the data file, it's on the 3rd line of the file.
    #     #F 06_19_Tony.dat
    #     #E 1403198515
    #     #D Thu Jun 19 12:21:55 2014
    if not os.path.exists(specFile):
        return None

    # read the first lines of the file and validate for SPEC data file format
    f = open(specFile, 'r')
    line = f.readline()
    if not line.startswith('#F '): return None
    line = f.readline()
    if not line.startswith('#E '): return None
    line = f.readline()
    if not line.startswith('#D '): return None
    f.close()

    return line[2:].strip()  # 'Thu Jun 19 12:21:55 2014'


def get_file_mtime(filename):
    '''
    get the file modified time from disk
    
    :param str fname: file name, already known to exist
    :return: time (float) fname was last modified
    '''
    return os.path.getmtime(filename)


def needToMakePlot(fullPlotFile, mtime_specFile):
    '''
    Determine if a plot needs to be (re)made.  Use mtime as the basis.

    :return bool: ``True`` if plot should be made again
    '''
    remake_plot = True
    if os.path.exists(fullPlotFile):
        mtime_plotFile = get_file_mtime(fullPlotFile)
        if mtime_plotFile > mtime_specFile:
            # plot was made after the data file was updated
            remake_plot = False     # don't remake the plot
    return remake_plot


def timestamp():
    '''
    current time as yyyy-mm-dd hh:mm:ss
    
    :return str: 
    '''
    ts = str(datetime.datetime.now())
    ts = ' '.join(ts.split('T'))    # convert to modified ISO8601 format
    ts = ts.split('.')[0]           # strip off the fractional seconds
    return ts


def build_index_html(specFile, plotList):
    '''
    build index.html content
    
    :param str specFile: name of SPEC data fmainile (relative or absolute)
    :param [str] plotList: list of HTML `<a>` elements, one for each plot image 
    '''
    baseSpecFile = os.path.basename(specFile)
    comment = "\n"
    comment += "   written by: %s\n" % sys.argv[0]
    comment += "   date: %s\n"       % timestamp()
    comment += "\n"

    href = "<a href='%s'>%s</a>" % (baseSpecFile, specFile)
    html  = "<html>\n"
    html += "  <head>\n"
    html += "    <title>SPEC scans from %s</title>\n" % specFile
    html += "    <!-- %s -->\n"                       % comment
    html += "  </head>\n"
    html += "  <body>\n"
    html += "    <h1>SPEC scans from: %s</h1>\n"      % specFile
    html += "\n"
    html += "    spec file: %s\n"                     % href
    html += "    <br />\n"
    html += "\n"
    html += "\n"
    html += "\n".join(plotList)
    html += "\n"
    html += "\n"
    html += "  </body>\n"
    html += "</html>\n"
    return html


def logger(message):
    '''
    log a message or report from this module

    :param str message: text to be logged
    '''
    now = str(datetime.datetime.now())
    name = os.path.basename(sys.argv[0])
    pid = os.getpid()
    text = "(%d,%s,%s) %s" % (pid, name, now, message)
    logging.info(text)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def main():
    import argparse
    global SPECPLOTS_DIR

    doc = __doc__.strip().splitlines()[0]
    p = argparse.ArgumentParser(description=doc)
    
    p.add_argument('specFiles',  
                        nargs='+',  
                        help="SPEC data file name(s)")
    
    pwd = os.getcwd()
    msg = 'base directory for output'
    msg += ' (default:' + pwd + ')'
    p.add_argument('-d', '--dir', help=msg)

    args = p.parse_args()

    specplots_dir = args.dir or pwd

    log_file = os.path.join(specplots_dir, 'specplot_files_processing.log')
    logging.basicConfig(filename=log_file, level=logging.INFO)

    logger('>'*10 + ' starting')
    PlotSpecFileScans(args.specFiles, specplots_dir)
    logger('<'*10 + ' finished')


def developer_main():
    path = '__plots__'
    if not os.path.exists(path):
        os.mkdir(path)
    sys.argv.append('-d')
    sys.argv.append(path)
    sys.argv.append('data/writer_1_3.h5')
#     sys.argv.append('data/02_03_setup.dat')
#     sys.argv.append('data/03_06_JanTest.dat')
#     sys.argv.append('data/lmn40.spe')
    main()


if __name__ == '__main__':
#     developer_main()
    main()
