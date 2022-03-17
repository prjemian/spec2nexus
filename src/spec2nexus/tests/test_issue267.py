import pathlib
import pytest

# from ._core import hfile
from .. import spec
from ..diffractometers import LatticeParameters2D
from ..diffractometers import Reflections2D

EXAMPLES = pathlib.Path(spec.__file__).absolute().parent / "data"
TESTFILE = EXAMPLES / "twoc.dat"


def test_testfile():
    assert EXAMPLES.exists()
    assert TESTFILE.exists()


@pytest.mark.parametrize(
    "n, scan_n, cmd",
    [
        [1, "1", "ascan  y -25.09 -13.09  20 2"],
        [2, "2", "loopscan 100 2 0"],
        [2.1, "2.1", "loopscan 100 2 0"],
    ],
)
def test_scan_commands(n, scan_n, cmd):
    sdf = spec.SpecDataFile(TESTFILE)
    assert sdf is not None
    assert len(sdf.getScanNumbers()) == 3
    assert len(sdf[:]) == 3

    scan = sdf[n]
    assert scan is not None
    assert scan.scanNum == scan_n
    assert scan.scanCmd == cmd

    assert hasattr(scan, "Q")
    assert len(scan.Q) == 2

    # no orientation matrix in twoc geometry
    assert not hasattr(scan, "UB")

    assert hasattr(scan, "diffractometer")
    twoc = scan.diffractometer
    assert twoc.geometry_name == "twoc"
    assert twoc.variant == "default"
    assert hasattr(twoc, "lattice")
    assert isinstance(twoc.lattice, LatticeParameters2D)
    assert len(twoc.lattice._fields) == 3
    for k in "a b gamma".split():
        assert hasattr(twoc.lattice, k)
    for k in "c alpha beta".split():
        assert not hasattr(twoc.lattice, k)
    assert hasattr(twoc, "reflections")
    assert len(twoc.reflections) == 1

    r0 = twoc.reflections[0]
    assert isinstance(r0, Reflections2D)
    assert len(r0._fields) == 4
    for k in "h k wavelength angles".split():
        assert hasattr(r0, k)
    assert not hasattr(r0, "l")
    assert len(r0.angles) == 2


def test_contents_s1():
    sdf = spec.SpecDataFile(TESTFILE)
    scan = sdf[1]
    assert round(scan.diffractometer.lattice.a, 4) == 6.2832
    assert round(scan.diffractometer.lattice.b, 4) == 6.2832
    assert round(scan.diffractometer.lattice.gamma, 4) == 90
    assert round(scan.diffractometer.reflections[0].h, 4) == 1
    assert round(scan.diffractometer.reflections[0].k, 4) == 0
    assert round(scan.diffractometer.reflections[0].wavelength, 4) == 0
    assert round(scan.diffractometer.reflections[0].angles["tth"], 4) == 60
    assert round(scan.diffractometer.reflections[0].angles["th"], 4) == 30
    assert round(scan.Q[0], 4) == 0.0026
    assert round(scan.Q[1], 4) == 0.0042
