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
Plot all ascan scans showing the time when plotted instead of scan command

This is a simple example of how to customize the scan macro handling.
There are many more ways to add complexity.
'''

import spec2nexus.specplot
import spec2nexus.specplot_gallery


class Custom_Ascan(spec2nexus.specplot.LinePlotter):
    '''
    simple customization
    '''

    def image(self, plotFile):
        'give a special subtitle'
        import datetime
        self.configure(subtitle='current time: ' + str(datetime.datetime.now()))
        # or an alternate, simpler value
        # self.configure(subtitle='<<this is the plot subtitle>>')
        
        # now, call the standard handling in the superclass
        spec2nexus.specplot.LinePlotter.image(self, plotFile)


def main():
    selector = spec2nexus.specplot.Selector()
    selector.add('ascan', Custom_Ascan)
    spec2nexus.specplot_gallery.main()


if __name__ == '__main__':
    main()
