"""
unit tests for the diffractometers module
"""


from ._core import EXAMPLES_PATH
from ._core import TEST_DATA_PATH
from .. import diffractometers
from .. import spec

from lxml import etree
import numpy
import os
import pathlib
import pytest


def test_dictionary():
    diffractometers.reset_geometry_catalog()
    assert diffractometers._geometry_catalog is None
    with pytest.raises(RuntimeError):
        diffractometers.DiffractometerGeometryCatalog()

    assert os.path.exists(diffractometers.DICT_FILE)

    dgc = diffractometers.get_geometry_catalog()
    assert len(dgc.db) == 20


def test_split_name_variation():
    nm, variant = diffractometers.split_name_variation("only")
    assert nm == "only"
    assert variant is None
    nm, variant = diffractometers.split_name_variation("two.parts")
    assert nm == "two"
    assert variant is not None
    assert variant == "parts"
    nm, variant = diffractometers.split_name_variation("more.than.two.parts")
    assert nm == "more.than.two.parts"
    assert variant is None


def test_class_DiffractometerGeometryCatalog():
    dgc1 = diffractometers.get_geometry_catalog()
    assert dgc1 == diffractometers._geometry_catalog
    dgc2 = diffractometers.get_geometry_catalog()
    assert dgc1 == dgc2
    diffractometers.reset_geometry_catalog()
    assert dgc1 != diffractometers._geometry_catalog
    assert dgc1 == dgc2
    assert diffractometers._geometry_catalog is None

    diffractometers.reset_geometry_catalog()
    dgc = diffractometers.get_geometry_catalog()
    assert dgc is not None
    assert dgc != dgc1
    assert dgc != dgc2

    expected = "DiffractometerGeometryCatalog(number=20)"
    assert str(dgc) == expected

    assert hasattr(dgc, "_default_geometry")
    assert dgc._default_geometry is not None
    assert dgc.get_default_geometry()["name"] == "spec"

    # spot tests verify method has_geometry()
    assert dgc.has_geometry("fourc")
    assert dgc.has_geometry("fourc.kappa")
    assert dgc.has_geometry("spec")
    assert not dgc.has_geometry("spec.kappa")
    assert dgc.has_geometry("psic.s2d2+daz")
    assert not dgc.has_geometry("s2d2.psic+daz")

    geos = dgc.geometries()
    expected = [
        "spec",
        "fivec",
        "fourc",
        "oscam",
        "pi1go",
        "psic",
        "s1d2",
        "s2d2",
        "sevc",
        "sixc",
        "surf",
        "suv",
        "trip",
        "twoc",
        "twoc_old",
        "w21h",
        "w21v",
        "zaxis",
        "zaxis_old",
        "zeta",
    ]
    assert len(geos), 20
    assert geos == expected

    geos = dgc.geometries(True)
    expected = [  # sorted
        "fivec.default",
        "fivec.kappa",
        "fourc.3axis",
        "fourc.default",
        "fourc.kappa",
        "fourc.omega",
        "fourc.picker",
        "fourc.xtalogic",
        "oscam.default",
        "pi1go.default",
        "psic.+daz",
        "psic.default",
        "psic.kappa",
        "psic.s2d2",
        "psic.s2d2+daz",
        "s1d2.default",
        "s2d2.default",
        "sevc.default",
        "sixc.default",
        "spec.default",
        "surf.default",
        "suv.default",
        "trip.default",
        "twoc.default",
        "twoc_old.default",
        "w21h.default",
        "w21v.d32",
        "w21v.default",
        "w21v.gmci",
        "w21v.id10b",
        "zaxis.default",
        "zaxis_old.beta",
        "zaxis_old.default",
        "zeta.default",
    ]
    assert len(geos) == 34
    assert sorted(geos) == expected

    for geo_name in dgc.geometries():
        msg = "name='%s' defined?" % geo_name
        geom = dgc.get(geo_name)
        assert "name" in geom, msg
        assert geom["name"] == geo_name, msg


@pytest.mark.parametrize(
    "base_path, filename, scan_number, geo_name, exc",
    [
        [TEST_DATA_PATH, "issue109_data.txt", -1, "fourc.default", None],  # 8-ID-I
        [TEST_DATA_PATH, "issue119_data.txt", -1, "spec.default", None],  # USAXS
        [TEST_DATA_PATH, "issue161_spock_spec_file", -1, "spec.default", None],  # SPOCK
        [TEST_DATA_PATH, "JL124_1.spc", -1, "sixc.default", None],
        [TEST_DATA_PATH, 'test_3_error.spec', -1, 'spec', etree.DocumentInvalid],  # UXML, has syntax error
        [TEST_DATA_PATH, "test_3.spec", -1, "spec", None],  # predates #o (mnemonics) lines
        [TEST_DATA_PATH, "test_4.spec", -1, "spec", None],  # predates #o (mnemonics) lines
        [EXAMPLES_PATH, "02_03_setup.dat", -1, "spec.default", None],
        [EXAMPLES_PATH, "03_06_JanTest.dat", -1, "spec.default", None],
        [EXAMPLES_PATH, "05_02_test.dat", -1, "spec.default", None],
        [EXAMPLES_PATH, "33bm_spec.dat", -1, "fourc.default", None],
        [
            EXAMPLES_PATH,
            "33id_spec.dat",
            -1,
            "spec",
            None,
        ],  # psic but predates #o (mnemonics) lines
        [EXAMPLES_PATH, "APS_spec_data.dat", -1, "spec.default", None],
        [EXAMPLES_PATH, "CdOsO", -1, "fourc.default", None],
        [EXAMPLES_PATH, "CdSe", -1, "fourc.default", None],
        [EXAMPLES_PATH, "lmn40.spe", -1, "spec", None],
        [EXAMPLES_PATH, "mca_spectra_example.dat", -1, "spec.default", None],
        [EXAMPLES_PATH, "spec_from_spock.spc", -1, "spec.default", None],
        [EXAMPLES_PATH, "startup_1.spec", 1, "spec", None],
        [EXAMPLES_PATH, "twoc.dat", 1, "twoc.default", None],
        [EXAMPLES_PATH, "usaxs-bluesky-specwritercallback.dat", -1, "spec.default", None],
        [EXAMPLES_PATH, "user6idd.dat", -1, "spec", None],  # predates #o (mnemonics) lines
        [EXAMPLES_PATH, "YSZ011_ALDITO_Fe2O3_planar_fired_1.spc", -1, "fourc.default", None],
    ],
)
def test_file_processing(base_path, filename, scan_number, geo_name, exc):
    dgc = diffractometers.get_geometry_catalog()
    fullname = os.path.join(base_path, filename)
    sdf = spec.SpecDataFile(fullname)
    assert sdf is not None

    scan = sdf.getScan(scan_number)
    assert scan is not None

    if exc is not None:
        with pytest.raises(exc):
            scan.interpret()
            dgc.match(scan)
            return

    geom = dgc.match(scan)
    assert geom is not None, filename
    assert geom == geo_name, filename

    gonio = diffractometers.Diffractometer(geom)
    gonio.parse(scan)

    if len(gonio.geometry_parameters) > 0:
        gpar = gonio.geometry_parameters
        for k in "g_aa g_bb g_cc g_al g_be g_ga LAMBDA".split():
            if k in gpar:
                assert gpar[k].value > 0, filename

        if "ub_matrix" in gpar:
            ub = gpar["ub_matrix"].value
            assert isinstance(ub, numpy.ndarray), filename
            assert ub.shape == (3, 3), filename


def test_class_Diffractometer():
    gonio = diffractometers.Diffractometer("big.little")
    assert gonio.geometry_name_full == "big.little"
    assert gonio.geometry_name == "big"
    assert gonio.variant == "little"
    assert gonio.geometry_parameters is not None


def test_print_str():
    DATA = pathlib.Path(__file__).absolute().parent.parent / "data"
    assert DATA.exists()

    TESTSCAN = 14
    TESTFILE = DATA / "33bm_spec.dat"
    TESTFILE.exists()

    sdf = spec.SpecDataFile(str(TESTFILE))
    scan = sdf.getScan(TESTSCAN)
    s = str(scan.diffractometer)
    assert s.startswith("Diffractometer(")
    assert "geometry=" in s
    assert "wavelength=" in s
    assert "mode=" in s
    assert "sector=" in s
    assert "h=" in s
    assert "k=" in s
    assert "l=" in s


def test_print_brief():
    DATA = pathlib.Path(__file__).absolute().parent.parent / "data"
    assert DATA.exists()

    TESTSCAN = 14
    TESTFILE = DATA / "33bm_spec.dat"
    TESTFILE.exists()

    sdf = spec.SpecDataFile(str(TESTFILE))
    scan = sdf.getScan(TESTSCAN)
    assert not scan.__interpreted__
    assert scan.scanCmd.startswith("hklscan")
    assert len(dir(scan)) == 62
    assert not scan.__interpreted__

    scan.interpret()
    assert scan.__interpreted__
    assert len(dir(scan)) == 66

    out = scan.diffractometer.print_brief(scan).strip()
    assert len(out) > 0
    out = out.splitlines()
    assert len(out) == 8
    assert out[0] == "fourc"
    assert out[1].startswith("h k l = ")
    assert out[2].startswith("alpha=")
    assert "alpha=" in out[2]
    assert "beta=" in out[2]
    assert "azimuth=" in out[2]
    assert "omega=" in out[3]
    assert "wavelength=" in out[3]
    assert out[4].startswith("2-theta = ")
    assert out[5].startswith("theta = ")
    assert out[6].startswith("chi = ")
    assert out[7].startswith("phi = ")


def test_print_all():
    DATA = pathlib.Path(__file__).absolute().parent.parent / "data"
    assert DATA.exists()

    TESTSCAN = 14
    TESTFILE = DATA / "33bm_spec.dat"
    TESTFILE.exists()

    sdf = spec.SpecDataFile(str(TESTFILE))
    scan = sdf.getScan(TESTSCAN)
    scan.interpret()

    out = scan.diffractometer.print_all(scan).strip()
    assert len(out) > 0
    out = out.splitlines()
    assert len(out) == 26
    expected = """
        SPEC file
        scan #
        SPEC scanCmd
        date
        geometry
        wavelength
        mode
        sector
        h
        k
        l
        lattice
        alpha
        beta
        azimuth
        omega
        full_geometry_name
        UB
        [
        [
        reflection 1
        reflection 2
        2-theta
        theta
        chi
        phi
    """.strip().splitlines()
    for i, k in enumerate([k.strip() for k in expected]):
        assert f"{k}" in out[i]
        assert out[i].strip().startswith(f"{k}")

# -----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014-2022, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
