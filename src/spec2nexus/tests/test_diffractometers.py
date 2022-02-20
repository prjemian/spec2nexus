"""
unit tests for the diffractometers module
"""

import numpy
import os
import pytest

from ._core import EXAMPLES_PATH
from ._core import TEST_DATA_PATH
from .. import spec
from .. import diffractometers


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
    "base_path, filename, scan_number, geo_name",
    [
        [TEST_DATA_PATH, "issue109_data.txt", -1, "fourc.default"],  # 8-ID-I
        [TEST_DATA_PATH, "issue119_data.txt", -1, "spec.default"],  # USAXS
        [TEST_DATA_PATH, "issue161_spock_spec_file", -1, "spec.default"],  # SPOCK
        [TEST_DATA_PATH, "JL124_1.spc", -1, "sixc.default"],
        # [TEST_DATA_DIR, 'test_3_error.spec', -1, 'spec'],                  # FIXME: #UXML, plugin has error
        [TEST_DATA_PATH, "test_3.spec", -1, "spec"],  # predates #o (mnemonics) lines
        [TEST_DATA_PATH, "test_4.spec", -1, "spec"],  # predates #o (mnemonics) lines
        [EXAMPLES_PATH, "02_03_setup.dat", -1, "spec.default"],
        [EXAMPLES_PATH, "03_06_JanTest.dat", -1, "spec.default"],
        [EXAMPLES_PATH, "05_02_test.dat", -1, "spec.default"],
        [EXAMPLES_PATH, "33bm_spec.dat", -1, "fourc.default"],
        [
            EXAMPLES_PATH,
            "33id_spec.dat",
            -1,
            "spec",
        ],  # psic but predates #o (mnemonics) lines
        [EXAMPLES_PATH, "APS_spec_data.dat", -1, "spec.default"],
        [EXAMPLES_PATH, "CdOsO", -1, "fourc.default"],
        [EXAMPLES_PATH, "CdSe", -1, "fourc.default"],
        [EXAMPLES_PATH, "lmn40.spe", -1, "spec"],
        [EXAMPLES_PATH, "mca_spectra_example.dat", -1, "spec.default"],
        [EXAMPLES_PATH, "spec_from_spock.spc", -1, "spec.default"],
        [EXAMPLES_PATH, "startup_1.spec", 1, "spec"],
        [EXAMPLES_PATH, "usaxs-bluesky-specwritercallback.dat", -1, "spec.default"],
        [EXAMPLES_PATH, "user6idd.dat", -1, "spec"],  # predates #o (mnemonics) lines
        [EXAMPLES_PATH, "YSZ011_ALDITO_Fe2O3_planar_fired_1.spc", -1, "fourc.default"],
    ],
)
def test_file_processing(base_path, filename, scan_number, geo_name):
    dgc = diffractometers.get_geometry_catalog()
    fullname = os.path.join(base_path, filename)
    scan = spec.SpecDataFile(fullname).getScan(scan_number)
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


# -----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014-2022, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
