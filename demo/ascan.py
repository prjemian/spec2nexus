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
Plot all scans that used `ascan`macro, showing only the scan number (not full scan command)

This is a simple example of how to customize the scan macro handling.
There are many more ways to add complexity.
'''

import spec2nexus.specplot
import spec2nexus.specplot_gallery


class Custom_Ascan(spec2nexus.specplot.LinePlotter):
    '''simple customization'''
    
    def get_plot_data(self):
        '''substitute with the data&time the plot was created'''
        structure = spec2nexus.specplot.LinePlotter.get_plot_data(self)
        text = '#S ' + str(self.scan.scanNum) + ' ascan'
        self.configure(subtitle = text)
        return structure


def main():
    selector = spec2nexus.specplot.Selector()
    selector.add('ascan', Custom_Ascan)
    spec2nexus.specplot_gallery.main()


if __name__ == '__main__':
    main()
