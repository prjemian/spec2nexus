"""Tests for the plugin module."""

import h5py
import os
import pathlib
import pytest

from . import _core
from ._core import hfile
from ._core import file_from_tests
from ._core import TEST_DATA_PATH
from ..control_lines import control_line_registry
from ..control_lines import ControlLines
from ..plugin_core import install_user_plugin
from .. import spec
from .. import writer


os.environ["SPEC2NEXUS_PLUGIN_PATH"] = "C://Users//Pete//Desktop, /tmp"
EXAMPLES = pathlib.Path(_core.EXAMPLES_PATH)


def test_plugin_handler_keys():
    h = control_line_registry.known_keys["#F"]
    assert h.key == "#F"


@pytest.mark.parametrize(
    "control_key, sample",
    [
        ["#S", r"#S 1 ascan eta 43.6355 44.0355 40 1"],
        ["#D", r"#D Thu Jul 17 02:38:24 2003"],
        ["#T", r"#T 1 (seconds)"],
        ["#G\\d+", r"#G0 0 0 0 0 0 1 0 0 0 0 0 0 50 0 0 0 1 0 0 0 0"],
        ["#V\\d+", r"#V110 101.701 56 1 4 1 1 1 1 992.253"],
        ["#N", r"#N 14"],
        [
            "#L",
            r"#L eta H K L elastic Kalpha Epoch seconds signal I00 harmonic signal2 I0 I0",
        ],
        ["#@MCA", r"#@MCA 16C"],
        ["#@CHANN", r"#@CHANN 1201 1110 1200 1"],
        [r"#o\d+", r"#o0 un0 mx my waxsx ax un5 az un7"],
        [r"@A\d*", r"@A 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\\"],
        [r"@A\d*", r"@A1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\\"],
        [r"@A\d*", r"@A2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\\"],
        ["scan_data", r" 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0".lstrip()],
        ["#H\\d+", r"#H4 FB_o2_on FB_o2_r FB_o2_sp"],
        [None, r"#Pete wrote this stuff"],
        [
            "scan_data",
            r"43.6835 0.998671 -0.0100246 11.0078 1 0 66 1 0 863 0 0 1225 1225",
        ],
        ["#@[cC][aA][lL][iI][bB]", r"#@CALIB 1 2 3"],
        ["#@[cC][aA][lL][iI][bB]", r"#@Calib 0.0501959 0.0141105 0 mca1"],
    ],
)
def test_plugin_get_control_key(control_key, sample):
    if control_key is not None:
        assert control_key in control_line_registry.known_keys
    value = control_line_registry.get_control_key(sample)
    if control_key is not None:
        assert value is not None, sample
    assert value == control_key


def test_custom_plugin():
    assert control_line_registry is not None
    assert isinstance(control_line_registry, ControlLines)
    num_known_control_lines_before = len(control_line_registry.lazy_attributes)
    assert num_known_control_lines_before != 0

    path = pathlib.Path(__file__).absolute().parent / "custom_plugins"
    assert path.exists()

    _filename = str(path / "specfile.txt")
    # custom_key = "#TEST"            # in SPEC data file
    # custom_attribute = "MyTest"     # in python, scan.MyTest

    # first, test data with custom control line without plugin loaded
    assert "#TEST" not in control_line_registry.known_keys
    assert "MyTest" not in control_line_registry.lazy_attributes
    sdf = spec.SpecDataFile(_filename)
    scan = sdf.getScan(50)
    assert "G0" in scan.G

    assert not hasattr(scan, "MyTest")
    with pytest.raises(AttributeError) as exc:
        assert len(scan.MyTest), 1
    expected = "'SpecDataFileScan' object has no attribute 'MyTest'"
    assert exc.value.args[0] == expected

    # next, test again after loading plugin
    install_user_plugin(path / "process_only_plugin.py")

    num_known_control_lines_after = len(control_line_registry.lazy_attributes)
    assert num_known_control_lines_after > num_known_control_lines_before
    assert "#TEST" in control_line_registry.known_keys
    assert "MyTest" in control_line_registry.lazy_attributes

    sdf = spec.SpecDataFile(_filename)
    scan = sdf.getScan(50)
    assert "G0" in scan.G

    assert hasattr(scan, "MyTest")
    assert len(scan.MyTest) == 1
    expected = "this is a custom control line to be found"
    assert scan.MyTest[0] == expected


def test_diffractometer_geometry_plugin(hfile):
    scan_number = 17
    sdf = spec.SpecDataFile(str(EXAMPLES / "33bm_spec.dat"))
    scan = sdf.getScan(scan_number)

    assert scan.diffractometer.geometry_name_full == "fourc.default"
    assert scan.diffractometer.mode == "Omega equals zero"
    assert scan.diffractometer.sector == 0
    assert scan.diffractometer.lattice is not None
    assert len(scan.diffractometer.reflections) == 2

    out = writer.Writer(sdf)
    out.save(hfile, [scan_number])

    with h5py.File(hfile, "r") as hp:
        nxentry = hp["/S17"]
        group = nxentry["instrument/geometry_parameters"]

        assert "instrument/name" in nxentry
        assert (
            nxentry["instrument/name"][0]
            == scan.diffractometer.geometry_name_full.encode()
        )
        checks = dict(
            diffractometer_simple=b"fourc",
            diffractometer_full=b"fourc.default",
            diffractometer_variant=b"default",
        )
        for k, v in checks.items():
            assert k in group
            assert group[k][0] == v

        for k in "g_aa g_bb g_cc g_al g_be g_ga LAMBDA".split():
            assert k in group
            v = group[k][()][0]
            assert v > 0

        assert "sample/unit_cell_abc" in nxentry
        assert "sample/unit_cell_alphabetagamma" in nxentry
        assert "sample/unit_cell" in nxentry

        assert "sample/ub_matrix" in nxentry
        ds = nxentry["sample/ub_matrix"]
        assert ds.shape == (3, 3)

        assert "sample/or0" in nxentry
        assert "sample/or0/h" in nxentry
        assert "sample/or0/k" in nxentry
        assert "sample/or0/l" in nxentry
        assert "sample/or1" in nxentry
        assert "sample/or1/h" in nxentry
        assert "sample/or1/k" in nxentry
        assert "sample/or1/l" in nxentry

        assert "instrument/monochromator/wavelength" in nxentry
        assert "sample/beam/incident_wavelength" in nxentry
        assert (
            nxentry["instrument/monochromator/wavelength"]
            == nxentry["sample/beam/incident_wavelength"]
        )


def test_empty_positioner():
    "issue #196"
    fname = file_from_tests("issue196_data.txt")
    assert os.path.exists(fname)
    scan_number = 108
    sdf = spec.SpecDataFile(fname)
    scan = sdf.getScan(scan_number)

    assert scan.header.raw.find("\n#O0 \n") > 0
    assert scan.header.raw.find("\n#o0 \n") > 0
    assert len(scan.header.O) == 1
    assert len(scan.header.O[0]) == 0
    assert len(scan.header.o) == 1
    assert len(scan.header.o[0]) == 0

    assert scan.raw.find("\n#P0 \n") > 0
    assert len(scan.P) == 1
    assert len(scan.P[0]) == 0
    assert len(scan.positioner) == 0


def test_nonempty_positioner():
    "issue #196"
    fname = file_from_tests("issue196_data2.txt")
    scan_number = 108
    sdf = spec.SpecDataFile(fname)
    scan = sdf.getScan(scan_number)

    assert scan.header.raw.find("\n#O0 \n") == -1
    assert scan.header.raw.find("\n#o0 \n") == -1
    assert scan.header.raw.find("\n#O0 m_stage_r\n") > 0
    assert scan.header.raw.find("\n#o0 mr\n") > 0
    assert len(scan.header.O) == 1
    assert len(scan.header.O[0]) == 1
    assert scan.header.O[0][0] == "m_stage_r"
    assert len(scan.header.o) == 1
    assert len(scan.header.o[0]) == 1
    assert scan.header.o[0][0] == "mr"
    assert scan.raw.find("\n#P0 \n") == -1
    assert scan.raw.find("\n#P0 8.824977\n") > 0
    assert len(scan.P) == 1
    assert len(scan.P[0]) == 1
    assert scan.P[0][0] == "8.824977"
    assert len(scan.positioner) == 1
    assert "m_stage_r" in scan.positioner
    assert scan.positioner["m_stage_r"] == float("8.824977")


# -----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014-2022, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
