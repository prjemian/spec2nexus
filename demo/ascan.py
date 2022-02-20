#!/usr/bin/env python

'''
Plot all scans that used the SPEC `ascan` macro, showing only the scan number (not full scan command)

This is a simple example of how to customize the scan macro handling.
There are many more ways to add complexity.
'''

import spec2nexus.specplot
import spec2nexus.specplot_gallery


class Custom_Ascan(spec2nexus.specplot.LinePlotter):
    '''simple customization'''
    
    def retrieve_plot_data(self):
        '''substitute with the data&time the plot was created'''
        import datetime
        spec2nexus.specplot.LinePlotter.retrieve_plot_data(self)
        self.set_plot_subtitle(str(datetime.datetime.now()))


def main():
    selector = spec2nexus.specplot.Selector()
    selector.add('ascan', Custom_Ascan)
    spec2nexus.specplot_gallery.main()


if __name__ == '__main__':
    main()

# -----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014-2022, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
