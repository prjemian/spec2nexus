"""Test issue 99."""

import os

from .. import specplot
from .. import spec

from ._core import EXAMPLES_PATH

TESTFILE = os.path.join(EXAMPLES_PATH, "lmn40.spe")


def test_specplot_lmn40_scan64():
    scan_number = 64
    expected_x_title = "L"

    sfile = specplot.openSpecFile(TESTFILE)
    assert isinstance(sfile, spec.SpecDataFile)

    scan = sfile.getScan(scan_number)
    assert isinstance(scan, spec.SpecDataFileScan)

    image_maker = specplot.Selector().auto(scan)
    assert issubclass(image_maker, specplot.ImageMaker)

    plotter = image_maker()
    assert isinstance(plotter, specplot.HKLScanPlotter)

    plotter.scan = scan
    plotter.set_plot_title(plotter.plot_title() or plotter.data_file_name())
    plotter.set_plot_subtitle(
        plotter.plot_subtitle()
        or "#" + str(plotter.scan.scanNum) + ": " + plotter.scan.scanCmd
    )
    plotter.set_timestamp(plotter.timestamp() or plotter.scan.date)

    plotter.retrieve_plot_data()
    plotter.plot_options()

    assert plotter.plottable()
    assert plotter.x_title() == expected_x_title
    assert plotter.y_title() == plotter.signal
    assert not plotter.x_log()
    assert not plotter.y_log()
    assert not plotter.z_log()
    assert plotter.plot_subtitle().startswith("#" + str(scan_number))


def test_specplot_lmn40_scan244():
    """Watch out for IndexError: list index out of range."""
    scan_number = 244
    expected_x_title = "data point number (hkl all held constant)"

    assert os.path.exists(TESTFILE)
    sfile = specplot.openSpecFile(TESTFILE)
    assert isinstance(sfile, spec.SpecDataFile)

    scan = sfile.getScan(scan_number)
    assert isinstance(scan, spec.SpecDataFileScan)

    image_maker = specplot.Selector().auto(scan)
    assert issubclass(image_maker, specplot.ImageMaker)

    plotter = image_maker()
    assert isinstance(plotter, specplot.HKLScanPlotter)

    plotter.scan = scan
    plotter.set_plot_title(plotter.plot_title() or plotter.data_file_name())
    plotter.set_plot_subtitle(
        plotter.plot_subtitle()
        or "#" + str(plotter.scan.scanNum) + ": " + plotter.scan.scanCmd
    )
    plotter.set_timestamp(plotter.timestamp() or plotter.scan.date)

    plotter.retrieve_plot_data()
    plotter.plot_options()

    assert plotter.plottable()
    assert plotter.x_title() == expected_x_title
    assert plotter.y_title() == plotter.signal
    assert not plotter.x_log()
    assert not plotter.y_log()
    assert not plotter.z_log()
    assert plotter.plot_subtitle().startswith("#" + str(scan_number))


# -----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014-2022, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
