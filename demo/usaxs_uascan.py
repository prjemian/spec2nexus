#!/usr/bin/env python

"""
Plot data from the USAXS uascan macro

.. autosummary::

    ~UAscan_Plotter

"""

import spec2nexus.specplot
import spec2nexus.specplot_gallery


class UAscan_Plotter(spec2nexus.specplot.LinePlotter):
    """Customized `uascan` handling"""

    def retrieve_plot_data(self):
        """plot the vertical axis on log scale"""
        spec2nexus.specplot.LinePlotter.retrieve_plot_data(self)

        if self.signal in self.data:
            # can't plot negative Y on log scale
            # Alternative to raising NotPlottable would be
            # to remove any data where Y <= 0
            if min(self.data[self.signal]) <= 0:
                msg = "cannot plot Y<0: " + str(self.scan)
                raise spec2nexus.specplot.NotPlottable(msg)

        # in the uascan, a name for the sample is given in `self.scan.comments[0]`
        self.set_y_log(True)
        self.set_plot_subtitle(
            "#%s uascan: %s" % (str(self.scan.scanNum), self.scan.comments[0])
        )


def debugging_setup():
    import os, sys
    import shutil
    import ascan

    selector = spec2nexus.specplot.Selector()
    selector.add("ascan", ascan.Custom_Ascan)  # just for the demo
    path = "__usaxs__"
    shutil.rmtree(path, ignore_errors=True)
    os.mkdir(path)
    sys.argv.append("-d")
    sys.argv.append(path)
    sys.argv.append(
        os.path.join("..", "src", "spec2nexus", "data", "APS_spec_data.dat")
    )


def main():
    selector = spec2nexus.specplot.Selector()
    selector.add("uascan", UAscan_Plotter)
    spec2nexus.specplot_gallery.main()


if __name__ == "__main__":
    # debugging_setup()
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
