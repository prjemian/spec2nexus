"""Tests for the spec module."""

import h5py
import numpy as np
import os
import pathlib
import platform
import pytest
import time

from . import _core
from ._core import EXAMPLES_PATH
from ._core import file_from_examples
from ._core import file_from_tests
from ._core import hfile
from ._core import TEST_DATA_PATH
from ._core import testpath
from .. import spec
from .. import utils
from .. import writer


# interval between file update and mtime reading
# at least a clock tick (1/60 s)
# or at least 1 second if not using float time for os.path.getmtime
SHORT_WAIT = 0.1


def is_spec_file(fname):
    return spec.is_spec_file(file_from_examples(fname))


def test_strip_first_word():
    assert utils.strip_first_word("one two three") == "two three"


def test_isSpecFileThis():
    assert not spec.is_spec_file("this_does_not_exist")
    assert not spec.is_spec_file(os.path.join(_core._ppath, "..", "spec2nexus"))
    assert not spec.is_spec_file(__file__)
    assert spec.is_spec_file(file_from_examples("APS_spec_data.dat"))
    assert not spec.is_spec_file_with_header("file does not exist")
    assert spec.is_spec_file_with_header(file_from_examples("APS_spec_data.dat"))
    assert not spec.is_spec_file_with_header(file_from_examples("spec_from_spock.spc"))


@pytest.mark.parametrize(
    "filename, expected",
    [
        ["33bm_spec.dat", True],
        ["33id_spec.dat", True],
        ["APS_spec_data.dat", True],
        ["CdSe", True],
        ["lmn40.spe", True],
        ["YSZ011_ALDITO_Fe2O3_planar_fired_1.spc", True],
        ["uxml", False],  # directory
        ["README.txt", False],  # text file
        ["33bm_spec.hdf5", False],
        ["33id_spec.hdf5", False],
        ["APS_spec_data.hdf5", False],
        ["compression.h5", False],
        ["Data_Q.h5", False],
        ["lmn40.hdf5", False],
        ["writer_1_3.h5", False],
    ],
)
def test_isSpecFile(filename, expected):
    """Test all the known data files to see if they are SPEC."""
    assert is_spec_file(filename) == expected, filename


@pytest.mark.parametrize(
    "trigger_exception, base_exception",
    [
        [spec.SpecDataFileNotFound, IOError],
        [spec.SpecDataFileCouldNotOpen, IOError],
        [spec.DuplicateSpecScanNumber, Exception],
        [spec.NotASpecDataFile, Exception],
        [spec.UnknownSpecFilePart, Exception],
    ],
)
def test_custom_exceptions(trigger_exception, base_exception):
    with pytest.raises(base_exception):
        raise trigger_exception()


def test_file_initial_exceptions():
    with pytest.raises(TypeError):
        spec.SpecDataFile()
    with pytest.raises(spec.SpecDataFileNotFound):
        spec.SpecDataFile("cannot_find_this_file")
    with pytest.raises(spec.SpecDataFileNotFound):
        spec.SpecDataFile(file_from_examples("03_05_UImg.dat"))
    with pytest.raises(spec.NotASpecDataFile):
        spec.SpecDataFile(__file__)


def test_33bm_spec():
    fname = file_from_examples("33bm_spec.dat")
    sfile = spec.SpecDataFile(fname)
    assert sfile.fileName == fname
    assert len(sfile.headers) == 1
    assert len(sfile.scans) == 17
    assert sfile.getMinScanNumber() == "1"
    assert sfile.getMaxScanNumber() == "17"
    assert len(sfile.getScan(1).L) == 27

    scan = sfile.getScan(1)
    assert scan.scanNum == "1"
    cmd = "ascan  th 19.022 19.222  60 -20000"
    assert scan.scanCmd == cmd
    assert sfile.getScanCommands([1, ]) == [
        "#S 1 " + cmd,
    ]
    x = "theta"
    y = "signal"
    assert scan.column_first == x
    assert scan.column_last == y
    assert len(scan.data[x]) == 61
    assert scan.data[x][0] == 19.022
    assert scan.data[y][0] == 0.0
    assert scan.data[x][-1] == 19.222
    assert scan.data[y][-1] == 0.0

    scan = sfile.getScan(-1)
    assert len(scan.positioner) == 22
    x = "2-theta"
    y = "m22"
    keys = list(scan.positioner.keys())
    assert keys[0] == x
    assert keys[-1] == y
    assert scan.positioner[x] == 67.78225
    assert scan.positioner[y] == 1230.0415
    # TODO: apply file-specific tests (see README.txt)
    # test hklscan (#14), hklmesh (#17)


def test_33id_spec():
    fname = file_from_examples("33id_spec.dat")
    sfile = spec.SpecDataFile(fname)
    assert sfile.fileName == fname
    assert len(sfile.headers) == 1
    assert len(sfile.scans) == 106
    assert sfile.getFirstScanNumber() == "1"
    assert sfile.getMinScanNumber() == "1"
    assert sfile.getMaxScanNumber() == "106"
    assert len(sfile.getScan(1).L) == 14
    scan = sfile.getScan(1)
    assert scan.scanNum == "1"
    cmd = "ascan  eta 43.6355 44.0355  40 1"
    assert scan.scanCmd == cmd
    assert sfile.getScanCommands([1, ]) == [
        "#S 1 " + cmd,
    ]
    assert scan.column_first == "eta"
    assert scan.column_last == "I0"
    assert len(scan.positioner) == 27
    assert len(scan.data["eta"]) == 41
    assert scan.data["eta"][0] == 43.628
    assert scan.data["I0"][0] == 1224.0
    assert scan.data["eta"][-1] == 44.0325
    assert scan.data["I0"][-1] == 1222.0
    scan = sfile.getScan(-1)
    assert scan.scanNum == str(106)
    assert len(scan.positioner) == 27
    assert scan.column_first == "Energy"
    assert scan.column_last == "I0"
    assert scan.positioner["DCM theta"] == 12.747328
    assert scan.positioner["ana.theta"] == -0.53981253


def test_MCA_single_spectrum():
    """Multiple MCA spectra."""
    fname = file_from_examples("33id_spec.dat")
    sfile = spec.SpecDataFile(fname)
    scan = sfile.getScan(1)

    assert not scan.__interpreted__
    assert "_mca" not in scan.data
    mca_spectra = scan.data["_mca_"]
    assert scan.__interpreted__

    rows = 41
    channels = 91
    assert "Epoch" in scan.data
    assert len(scan.data["Epoch"]) == rows
    assert "_mca_" in scan.data

    mca = "mca"
    assert mca in mca_spectra
    assert len(mca_spectra[mca]) == rows
    assert len(mca_spectra[mca][0]) == channels

    spectra = np.array(scan.data["_mca_"][mca])
    assert spectra.shape == (rows, channels)
    assert spectra.min() == 0
    assert spectra.max() == 0  # ALL of these spectra are zero


def test_MCA_multiple_spectra():
    """Multiple MCA spectra."""
    fname = file_from_examples("mca_spectra_example.dat")
    sfile = spec.SpecDataFile(fname)
    scan = sfile.getScan(1)

    assert not scan.__interpreted__
    scan.interpret()
    assert scan.__interpreted__

    # 1353 data rows, 4 MCAs, each with 256 channels (so 1353x256 arrays)
    num_MCAs = 4
    rows = 1353
    channels = 256
    assert "Epoch" in scan.data
    assert len(scan.data["Epoch"]) == rows
    assert "_mca_" in scan.data
    for n in range(num_MCAs):
        mca = f"mca{n+1}"
        assert mca in scan.data["_mca_"]
        assert len(scan.data["_mca_"][mca]) == rows
        assert len(scan.data["_mca_"][mca][0]) == channels

        spectra = np.array(scan.data["_mca_"][mca])
        assert spectra.shape == (rows, channels)
        assert spectra.min() == 0
        assert spectra.max() > 0


def test_APS_spec_data():
    """UNICAT metadata."""
    fname = file_from_examples("APS_spec_data.dat")
    sfile = spec.SpecDataFile(fname)
    assert sfile.fileName == fname
    assert len(sfile.headers) == 1
    assert len(sfile.scans) == 20
    assert sfile.getMinScanNumber() == "1"
    assert sfile.getMaxScanNumber() == "20"
    assert len(sfile.getScan(1).L) == 15
    scan = sfile.getScan(1)
    assert scan.scanNum == "1"
    cmd = "ascan  mr 15.6102 15.6052  30 0.3"
    assert scan.scanCmd == cmd
    assert sfile.getScanCommands([1, ]) == [
        "#S 1 " + cmd,
    ]
    x = "mr"
    y = "I0"
    assert scan.column_first == x
    assert scan.column_last == y
    assert len(scan.data[x]) == 31
    assert scan.data[x][0] == 15.6102
    assert scan.data[y][0] == 222.0
    assert scan.data[x][-1] == 15.6052
    assert scan.data[y][-1] == 255.0
    scan = sfile.getScan(-1)
    assert scan.scanNum == str(20)
    assert len(scan.positioner) == 47
    assert scan.column_first == "ar"
    assert scan.column_last == "USAXS_PD"
    assert scan.positioner["sa"] == -8.67896
    assert scan.positioner["sx_fine"] == -14.4125
    # TODO: apply file-specific tests (see README.txt)
    # uascan (#5), UNICAT metadata (#5)


def test_CdSe():
    fname = file_from_examples("CdSe")
    sfile = spec.SpecDataFile(fname)
    assert sfile.fileName == fname
    assert len(sfile.headers) == 1
    assert len(sfile.scans) == 102
    assert sfile.getMinScanNumber() == "1"
    assert sfile.getMaxScanNumber() == "102"
    assert len(sfile.getScan(1).L) == 55
    scan = sfile.getScan(1)
    assert scan.scanNum == "1"
    cmd = "ascan  herixE -5 5  40 1"
    assert scan.scanCmd == cmd
    assert sfile.getScanCommands([1, ]) == [
        "#S 1 " + cmd,
    ]
    x = "HerixE"
    y = "Seconds"
    assert scan.column_first == x
    assert scan.column_last == y
    assert len(scan.data[x]) == 39
    assert scan.data[x][0] == -5.0137065
    assert scan.data[y][0] == 1.0
    assert scan.data[x][-1] == 4.4971428
    assert scan.data[y][-1] == 1.0
    scan = sfile.getScan(-1)
    assert scan.scanNum == str(102)
    assert len(scan.positioner) == 138
    assert scan.column_first == "HerixE"
    assert scan.column_last == "Seconds"
    assert scan.positioner["cam-x"] == 2.06
    assert scan.positioner["rbs_xy"] == -4.4398827
    # TODO: apply file-specific tests (see README.txt)
    # 1-D scans (ascan), problem with scan abort on lines 5918-9, in scan 92


def test_lmn40():
    fname = file_from_examples("lmn40.spe")
    sfile = spec.SpecDataFile(fname)
    assert sfile.fileName == fname
    assert len(sfile.headers) == 2  # TODO: test more here!
    assert len(sfile.scans) == 262
    assert sfile.getMinScanNumber() == "1"
    assert sfile.getMaxScanNumber() == "271"
    assert len(sfile.getScan(1).L) == 9
    scan = sfile.getScan(1)
    assert scan.scanNum == "1"
    cmd = "ascan  tth -0.7 -0.5  101 1"
    assert scan.scanCmd == cmd
    assert sfile.getScanCommands([1, ]) == [
        "#S 1 " + cmd,
    ]
    x = "Two Theta"
    y = "winCZT"
    assert scan.column_first == x
    assert scan.column_last == y
    assert len(scan.data[x]) == 50
    assert scan.data[x][0] == -0.70000003
    assert scan.data[y][0] == 1.0
    assert scan.data[x][-1] == -0.60300003
    assert scan.data[y][-1] == 11.0
    scan = sfile.getScan(-1)
    assert scan.scanNum == str(271)
    assert len(scan.positioner) == 17
    assert scan.column_first == "phi"
    assert scan.column_last == "NaI"
    assert scan.positioner["chi"] == 90.000004
    assert scan.positioner["Two Theta"] == 0.15500001
    # TODO: apply file-specific tests (see README.txt)
    # two #E lines, has two header sections
    # number of scans != maxScanNumber, something missing?


def test_YSZ011_ALDITO_Fe2O3_planar_fired_1():
    fname = file_from_examples("YSZ011_ALDITO_Fe2O3_planar_fired_1.spc")
    sfile = spec.SpecDataFile(fname)
    assert sfile.fileName == fname
    assert len(sfile.headers) == 1
    assert len(sfile.scans) == 37
    assert sfile.getMinScanNumber() == "1"
    assert sfile.getMaxScanNumber() == "37"
    assert len(sfile.getScan(1).L) == 50
    scan = sfile.getScan(1)
    assert scan.scanNum == "1"
    cmd = "ascan  th 26.7108 27.1107  60 0.05"
    assert scan.scanCmd == cmd
    assert sfile.getScanCommands([1, ]) == [
        "#S 1 " + cmd,
    ]
    x = "theta"
    y = "imroi1"
    assert scan.column_first == x
    assert scan.column_last == y
    assert len(scan.data[x]) == 60
    assert scan.data[x][0] == 26.714
    assert scan.data[y][0] == 6.0
    assert scan.data[x][-1] == 27.1075
    assert scan.data[y][-1] == 7.0
    scan = sfile.getScan(-1)
    assert scan.scanCmd == "ascan  phi -180 180  720 0.5"
    assert len(scan.positioner) == 26
    x = "2-theta"
    y = "chSens"
    keys = list(scan.positioner.keys())
    assert keys[0] == x
    assert keys[-1] == y
    assert scan.positioner[x] == 18.8
    assert scan.positioner[y] == 5.0
    # TODO: apply file-specific tests (see README.txt)
    # 1-D scans, text in #V35.2 metadata (powderMotor="theta" others are float), also has #UIM control lines


def test_extra_control_line_content__issue109():
    specFile = file_from_tests("issue109_data.txt")
    assert os.path.exists(specFile)
    sfile = spec.SpecDataFile(specFile)

    scan_number = 1
    scan = sfile.getScan(scan_number)
    assert scan is not None
    assert scan.T == "0.5", "received expected count time"

    # check scan 25, #T line said 0 seconds, but data for Seconds says 1
    scan_number = 25
    scan = sfile.getScan(scan_number)
    assert scan is not None
    assert scan.T == "0", "received expected count time"
    assert "Seco nds" in scan.data, "found counting base"
    assert scan.data["Seco nds"][0] == 1, "received expected count time"
    assert scan.T != str(
        scan.data["Seco nds"][0]
    ), "did not report what they were about to do"

    # check scan 11, #M line said 400000 counts
    scan_number = 11
    scan = sfile.getScan(scan_number)
    assert scan is not None
    assert scan.M == "400000", "received expected monitor count"
    assert hasattr(scan, "MCA"), "MCA found"
    assert "ROI" in scan.MCA, "MCA ROI found"
    roi_dict = scan.MCA["ROI"]
    key = "FeKa(mca1 R1)"
    assert key in roi_dict, "MCA ROI config found"
    roi = roi_dict[key]
    assert roi["first_chan"] == 377, "MCA ROI first channel"
    assert roi["last_chan"] == 413, "MCA ROI last channel"

    assert key in scan.data, "MCA ROI data found"
    assert len(scan.data[key]) == 61, "embedded comment not part of data"


@pytest.mark.parametrize("filename", [None, "issue109_data.txt"])
def test_str_parm(filename):
    if filename is None:
        specFile = None
    else:
        specFile = file_from_tests(filename)
        assert os.path.exists(specFile)
    sdf = spec.SpecDataFile(specFile)
    assert os.path.basename(str(sdf)) == str(filename)
    if filename is not None:
        assert str(sdf) == sdf.fileName


def test_specfile_update_available(testpath):
    """test the ``update_available`` property"""
    spec_file = _core.getActiveSpecDataFile(testpath)

    sdf = spec.SpecDataFile(spec_file)
    assert sdf.mtime > 0
    assert not sdf.update_available
    if platform.system() == "Windows":
        expected = 1877  # 2-byte EOL
    else:
        expected = 1837  # 1-byte EOL
    assert sdf.filesize == expected
    assert sdf.last_scan == sdf.getLastScanNumber()
    assert sdf.last_scan == "3"

    # update the file with more data
    _core.addMoreScans(spec_file)
    time.sleep(SHORT_WAIT)

    assert sdf.update_available


def test_specfile_refresh(testpath):
    spec_file = _core.getActiveSpecDataFile(testpath)
    sdf = spec.SpecDataFile(spec_file)
    assert sdf.last_scan is not None
    assert len(sdf.getScanNumbers()) == 3
    if platform.system() == "Windows":
        expected = 1877  # 2-byte EOL
    else:
        expected = 1837  # 1-byte EOL
    assert sdf.filesize == expected

    # update the file with more data
    _core.addMoreScans(spec_file)
    time.sleep(SHORT_WAIT)

    scan_number = sdf.refresh()
    if platform.system() == "Windows":
        expected = 4085  # 2-byte EOL
    else:
        expected = 4013  # 1-byte EOL
    assert sdf.filesize == expected
    assert len(sdf.getScanNumbers()) == 5
    assert scan_number is not None
    assert sdf.last_scan is not None
    assert scan_number != sdf.last_scan
    assert scan_number != sdf.getLastScanNumber()
    assert sdf.last_scan == sdf.getLastScanNumber()

    time.sleep(SHORT_WAIT)
    scan_number = sdf.refresh()
    assert scan_number is None
    assert len(sdf.getScanNumbers()) == 5


@pytest.mark.parametrize(
    "filename, given, scanlist",
    [
        ["CdOsO", "5", ["5", ]],
        ["CdOsO", ":4", ["1", "2", "3", "1.1"]],
        ["CdOsO", ":4:", ["1", "2", "3", "1.1"]],
        ["CdOsO", ":4:0", ["1", "2", "3"]],
        ["CdOsO", ":4:1", ["1.1"]],
        ["CdOsO", ":4:-1", ["1.1", "2", "3"]],
        ["CdOsO", "-5:", ["69", "70", "71", "72", "73"]],
        ["CdOsO", "-1", ["73", ]],
        ["user6idd.dat", "::", ["1", "2"]],
        ["33bm_spec.dat", "-1", ["17", ]],
        ["33bm_spec.dat", "6", ["6", ]],
        ["33bm_spec.dat", "5:11", ["5", "6", "7", "8", "9", "10"]],
        ["33bm_spec.dat", "9:11, 1:4, 7, -5", ["9", "10", "1", "2", "3", "7", "13"]],
        ["20220311-161530.dat", "::0", ["2", "3", "4", "1", "5"]],
        ["20220311-161530.dat", "2", ["2", ]],
        ["20220311-161530.dat", "4.3", ["4.3", ]],
        ["20220311-161530.dat", "4.10", ["4.1", ]],
        ["20220311-161530.dat", "'4.10'", ["4.10", ]],
        ["20220311-161530.dat", "3,4.3,'4.10'", "3,4.3,4.10".split(",")],
        ["20220311-161530.dat", "4.8,4.9,'4.10',4.11", "4.8,4.9,4.10,4.11".split(",")],
        ["20220311-161530.dat", "-5,5", ["1.14", "5"]],
        ["20220311-161530.dat", "-5:", ["1.14", "2.15", "3.15", "4.15", "5.14"]],
        ["20220311-161530.dat", "::-1", ["2.15", "3.15", "4.15", "1.14", "5.14"]],
        ["20220311-161530.dat", "::15", ["2.15", "3.15", "4.15"]],
        ["20220311-161530.dat", "::1", ["2.1", "3.1", "4.1", "1.1", "5.1"]],
    ]
)
def test_slicing(filename, given, scanlist):
    sdf = spec.SpecDataFile(file_from_examples(filename))
    scans = eval(f"sdf[{given}]")
    if not isinstance(scans, list):
        scans = [scans]
    assert isinstance(scans, list)
    assert len(scans) == len(scanlist), given

    expected = [sdf.getScan(n) for n in scanlist]
    for s, e in zip(scans, expected):
        assert s == e, f"given={given}  s='{s.date}' = e='{e.date}'"


@pytest.mark.parametrize(
    "filename, given, error",
    [
        ["CdOsO", "", SyntaxError],
        ["CdOsO", None, TypeError],
        ["CdOsO", "1:-1", IndexError],
        ["CdOsO", "-1:1", IndexError],
    ]
)
def test_slicing_errors(filename, given, error):
    with pytest.raises(error):
        eval(
            f"spec.SpecDataFile(file_from_examples('{filename}'))[{given}]"
        )


@pytest.mark.parametrize(
    "specFile, scan_number, contents",
    [
        [f"{EXAMPLES_PATH}/user6idd.dat", 2, ["2"]],
        [f"{EXAMPLES_PATH}/user6idd.dat", 1, None],
        [
            f"{TEST_DATA_PATH}/issue109_data.txt",
            11,
            [(
                "11  Max: 83356  at 5.469   FWHM: 0.0165099"
                "  at 5.48551   COM: 5.48525   SUM: 3.47646e+06"
            )]
        ],
    ]
)
def test_user_results__issue263(specFile, scan_number, contents, hfile):
    assert os.path.exists(specFile)

    sdf = spec.SpecDataFile(specFile)
    assert isinstance(sdf, spec.SpecDataFile)

    scan = sdf.getScan(scan_number)
    assert isinstance(scan, spec.SpecDataFileScan)

    assert not scan.__interpreted__, (specFile, scan_number)

    scan.interpret()
    assert scan.__interpreted__, (specFile, scan_number)

    if contents is None:
        assert not hasattr(scan, "R"), (specFile, scan_number)
    else:
        assert hasattr(scan, "R"), (specFile, scan_number)
        assert scan.R == contents, (specFile, scan_number)

    # test HDF5 file
    specwriter = writer.Writer(sdf)
    specwriter.save(hfile, [scan_number])
    assert pathlib.Path(hfile).exists()
    with h5py.File(hfile, "r") as root:
        entry_name = f"/S{scan_number}"
        assert entry_name in root

        entry = root[entry_name]
        key = "UserResults"
        if contents is None:
            assert key not in entry
        else:
            assert key in entry

            note = entry[key]
            assert note.attrs.get("NX_class") == "NXnote"
            assert len(note) == len(contents)

            for i, item in enumerate(contents, start=1):
                item_name = f"item_{i}"
                assert item_name in note

                v = note[item_name][()][0].decode()
                assert v == item, (specFile, scan_number, item_name, item, v)


# ----------------------
# -------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014-2022, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
