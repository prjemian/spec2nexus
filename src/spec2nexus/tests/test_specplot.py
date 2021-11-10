"""Tests for the specplot module."""

# -----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014-2020, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------

import os
import pytest
import shutil
import sys
import time

from . import _core
from ._core import tempdir
from .. import specplot


ARGV0 = sys.argv[0]


def abs_data_fname(fname):
    return os.path.join(_core.EXAMPLES_DIR, fname)


# class Issue_66_plotting_problems():
#     def setUp():
#         self.basepath = os.path.join(_path, "spec2nexus")
#         self.datapath = os.path.join(self.basepath, "data")
#         self.plotFile = tests.common.create_test_file(suffix=".png")
#         sys.argv = [
#             sys.argv[0],
#         ]

#     def tearDown():
#         if os.path.exists(self.plotFile):
#             os.remove(self.plotFile)

#     #     def testName():
#     #         pass


def test_scan_aborted_after_0_points(tempdir):
    spec_file = abs_data_fname("33bm_spec.dat")
    scan_number = 15

    sdf = specplot.openSpecFile(spec_file)
    scan = sdf.getScan(scan_number)
    assert scan is not None
    plotter = specplot.LinePlotter()

    plot_file = os.path.join(tempdir, "spec_plot.png")
    if os.path.exists(plot_file):  # always re-create this plot for testing
        os.remove(plot_file)

    with pytest.raises(specplot.NoDataToPlot):
        plotter.plot_scan(scan, plot_file)

    assert not os.path.exists(plot_file)


def test_y_values_all_zero_lin_lin(tempdir):
    spec_file = os.path.join(_core.TEST_DATA_DIR, "issue64_data.txt")
    scan_number = 50
    assert os.path.exists(spec_file)

    sdf = specplot.openSpecFile(spec_file)
    scan = sdf.getScan(scan_number)
    assert scan is not None
    plotter = specplot.LinePlotter()

    plot_file = os.path.join(tempdir, "spec_plot.png")
    if os.path.exists(plot_file):  # always re-create this plot for testing
        os.remove(plot_file)

    plotter.plot_scan(scan, plot_file)
    assert os.path.exists(plot_file)


def test_y_values_all_zero_log_lin(tempdir):
    spec_file = os.path.join(_core.TEST_DATA_DIR, "issue64_data.txt")
    scan_number = 50

    sfile = specplot.openSpecFile(spec_file)
    scan = sfile.getScan(scan_number)
    assert scan is not None
    plotter = specplot.LinePlotter()

    plot_file = os.path.join(tempdir, "spec_plot.png")
    if os.path.exists(plot_file):  # always re-create this plot for testing
        os.remove(plot_file)

    plotter.set_y_log(True)
    with pytest.raises(ValueError):
        plotter.plot_scan(scan, plot_file)
    assert not os.path.exists(plot_file)


def test_command_line(tempdir):
    spec_file = abs_data_fname("02_03_setup.dat")
    plot_file = os.path.join(tempdir, "spec_plot.png")
    sys.argv = [ARGV0, spec_file, "1", plot_file]

    specplot.main()
    assert os.path.exists(plot_file)

    shutil.rmtree(tempdir, ignore_errors=True)
    assert not os.path.exists(plot_file)


@pytest.mark.parametrize(
    "filename, scan_number",
    [
        ["33id_spec.dat", 22],  # issue 72 -- mesh
        ["33bm_spec.dat", 17],  # issue 72 -- hklmesh
        ["33bm_spec.dat", 14],  # issue 80 -- hklscan, l
    ]
)
def test_command_line_plot(filename, scan_number, tempdir):
    specFile = abs_data_fname(filename)

    plot_file = os.path.join(tempdir, "image.png")
    sys.argv = [ARGV0, specFile, str(scan_number), plot_file]

    specplot.main()
    assert os.path.exists(plot_file)


def test_one_line_mesh_scan_as_1D_plot_issue82(tempdir):
    spec_file = os.path.join(_core.TEST_DATA_DIR, "issue82_data.txt")
    scan_number = 17

    sdf = specplot.openSpecFile(spec_file)
    scan = sdf.getScan(scan_number)
    assert scan is not None

    image_maker = specplot.Selector().auto(scan)
    assert issubclass(image_maker, specplot.ImageMaker)

    plotter = image_maker()
    assert isinstance(plotter, specplot.MeshPlotter)

    plot_file = os.path.join(tempdir, "spec_plot.png")
    if os.path.exists(plot_file):  # always re-create this plot for testing
        os.remove(plot_file)

    plotter.plot_scan(scan, plot_file)
    assert os.path.exists(plot_file)


def test_one_line_mesh_scan_type_error_33id_29(tempdir):
    spec_file = abs_data_fname("33id_spec.dat")
    scan_number = 29

    sdf = specplot.openSpecFile(spec_file)
    scan = sdf.getScan(scan_number)
    assert scan is not None

    image_maker = specplot.Selector().auto(scan)
    assert issubclass(image_maker, specplot.ImageMaker)

    plotter = image_maker()
    assert isinstance(plotter, specplot.MeshPlotter)

    plot_file = os.path.join(tempdir, "spec_plot.png")
    if os.path.exists(plot_file):  # always re-create this plot for testing
        os.remove(plot_file)

    plotter.plot_scan(scan, plot_file)
    assert os.path.exists(plot_file)


def test_40x35_grid_shown_properly_lmn40_spe(tempdir):
    spec_file = abs_data_fname("lmn40.spe")
    scan_number = 14

    sdf = specplot.openSpecFile(spec_file)
    scan = sdf.getScan(scan_number)
    assert scan is not None

    image_maker = specplot.Selector().auto(scan)
    assert issubclass(image_maker, specplot.ImageMaker)

    plotter = image_maker()
    assert isinstance(plotter, specplot.MeshPlotter)

    plot_file = os.path.join(tempdir, "spec_plot.png")
    if os.path.exists(plot_file):  # always re-create this plot for testing
        os.remove(plot_file)

    plotter.plot_scan(scan, plot_file)
    assert os.path.exists(plot_file)


def test_refresh(tempdir):
    plot = os.path.join(tempdir, "plot.svg")
    plot2 = os.path.join(tempdir, "plot2.svg")

    spec_file = _core.getActiveSpecDataFile(tempdir)

    sdf = specplot.openSpecFile(spec_file)
    scan = sdf.getScan(3)
    plotter = specplot.LinePlotter()

    # plot the first data
    plotter.plot_scan(scan, plot)
    assert os.path.exists(plot)
    plotsize = os.path.getsize(plot)
    mtime = os.path.getmtime(plot)
    assert plotsize > 0
    assert mtime > 0

    for iter in range(2):
        scan_number = sdf.refresh()
        if scan_number is None:
            scan = sdf.getScan(3)
            assert scan.__interpreted__
            # update the file with more data
            _core.addMoreScans(spec_file)
            time.sleep(0.1)
        else:
            scan = sdf.getScan(3)
            assert not scan.__interpreted__
            plotter.plot_scan(scan, plot2)
            assert os.path.exists(plot2)
            assert os.path.getmtime(plot2) > mtime
            assert os.path.getsize(plot2) != plotsize
