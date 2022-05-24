#!/usr/bin/env python

"""
Plot data from the USAXS FlyScan macro.

.. autosummary::

    ~read_reduced_fly_scan_file
    ~retrieve_flyScanData
    ~USAXS_FlyScan_Structure
    ~USAXS_FlyScan_Plotter

"""

import h5py
import numpy
import pathlib

import spec2nexus.specplot
import spec2nexus.specplot_gallery

# $URL: https://subversion.xray.aps.anl.gov/small_angle/USAXS/livedata/specplot.py $
REDUCED_FLY_SCAN_BINS = 250  # the default
PLOT_AXES = ["Q", "R"]


# methods picked (& modified) from the USAXS livedata project
def read_reduced_fly_scan_file(hdf5_file_name):
    """
    Read any and all reduced data from the HDF5 file, return in a dictionary.

    dictionary = {
      'full': (dictionary keys: Q, R, R_max, ar, fwhm, centroid)
      '250':  (dictionary keys: Q, R, dR)
      '5000': (dictionary keys: Q, R, dR)
    }
    """

    reduced = {}
    with h5py.File(str(hdf5_file_name), "r") as hdf:
        entry = hdf["/entry"]
        for key in entry.keys():
            if key.startswith("flyScan_reduced_"):
                nxdata = entry[key]
                d = {}
                for dsname in PLOT_AXES:
                    if dsname in nxdata:
                        value = nxdata[dsname]
                        if value.size == 1:
                            d[dsname] = float(value[0])
                        else:
                            d[dsname] = numpy.array(value)
                reduced[key[len("flyScan_reduced_") :]] = d
    return reduced


def retrieve_flyScanData(scan):
    """Retrieve reduced, rebinned data from USAXS Fly Scans."""
    comment = scan.comments[2]
    key_string = "FlyScan file name = "
    index = comment.find(key_string) + len(key_string)

    hdf_file_name = comment[index:-1]
    path = pathlib.Path(scan.header.parent.fileName).parent
    abs_file = (path / hdf_file_name).absolute()

    plotData = {}
    if abs_file.exists():
        reduced = read_reduced_fly_scan_file(abs_file)
        s_num_bins = str(REDUCED_FLY_SCAN_BINS)

        choice = reduced.get(s_num_bins) or reduced.get("full")

        if choice is not None:
            plotData = {axis: choice[axis] for axis in PLOT_AXES}

    return plotData


class USAXS_FlyScan_Plotter(spec2nexus.specplot.LinePlotter):
    """
    Customize `FlyScan` handling, plot :math:`log(I)` *vs.* :math:`log(Q)`.

    The USAXS FlyScan data is stored in a NeXus HDF5 file in a subdirectory
    below the SPEC data file.  This code uses existing code from the
    USAXS instrument to read that file.
    """

    def retrieve_plot_data(self):
        """Retrieve reduced data from the FlyScan's HDF5 file."""
        # get the data from the HDF5 file
        fly_data = retrieve_flyScanData(self.scan)

        if len(fly_data) != 2:
            raise spec2nexus.specplot.NoDataToPlot(str(self.scan))

        self.signal = "R"
        self.axes = ["Q"]
        self.data = fly_data

        # customize the plot just a bit
        # sample name as given by the user?
        subtitle = "#" + str(self.scan.scanNum)
        subtitle += " FlyScan: " + self.scan.comments[0]
        self.set_plot_subtitle(subtitle)
        self.set_x_log(True)
        self.set_y_log(True)
        self.set_x_title(r"$|\vec{Q}|, 1/\AA$")
        self.set_y_title(r"USAXS $R(|\vec{Q}|)$, a.u.")

    def plottable(self):
        """
        Can this data be plotted as expected?
        """
        if self.signal in self.data:
            signal = self.data[self.signal]
            if signal is not None and len(signal) > 0 and len(self.axes) == 1:
                if len(signal) == len(self.data[self.axes[0]]):
                    return True
        return False


def debugging_setup():
    import sys
    import shutil

    path = pathlib.Path("..") / "src"
    sys.path.insert(0, str(path))
    path = "__usaxs__"
    shutil.rmtree(path, ignore_errors=True)
    pathlib.os.mkdir(path)
    sys.argv.append("-d")
    sys.argv.append(path)
    data_file = path / "spec2nexus" / "data" / "02_03_setup.dat"
    sys.argv.append(str(data_file.absolute()))


def main():
    selector = spec2nexus.specplot.Selector()
    selector.add("FlyScan", USAXS_FlyScan_Plotter)
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
