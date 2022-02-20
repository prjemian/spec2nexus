"""Tests for the extractSpecScan module."""

import os
import pytest
import sys

from ._core import EXAMPLES_PATH
from .. import extractSpecScan


# os.environ["SPEC2NEXUS_PLUGIN_PATH"] = "C://Users//Pete//Desktop, /tmp"


def test_CdSe_scan_92(capsys):
    fname = os.path.join(EXAMPLES_PATH, "CdSe")
    sys.argv = [sys.argv[0], fname]
    sys.argv.append("-s")
    sys.argv.append("92")
    sys.argv.append("-c")
    columns = "HerixE T_sample_LS340 HRMpzt1".split()
    sys.argv += columns

    extractSpecScan.main()  # scan #92 was aborted
    out, _err = capsys.readouterr()
    assert isinstance(out, str)
    out = out.strip().splitlines()

    for item, text in enumerate("program: read: wrote:".split()):
        assert out[item].startswith(text)

    outfile = out[2][len("wrote: "):]
    assert os.path.exists(outfile)
    buf = open(outfile, "r").readlines()

    assert len(buf) == 22, "number of lines in data file"
    assert (
        "# file: " + fname == buf[0].strip()
    ), "original SPEC data file name in data file"
    assert "# scan: 92" == buf[1].strip(), "scan number in data file"
    assert "# " + "\t".join(columns) == buf[2].strip(), "column labels in data file"

    # test first and last lines of data
    # remaining lines: three columns of numbers, tab delimited
    checks = [
        # line  [expected 3 values]
        [3, [-10.118571, 297.467, 66.0]],  # first line
        [-1, [-5.5910424, 297.483, 66.0]],  # last line
    ]
    for line_number, expected in checks:
        got = list(map(float, buf[line_number].split()))
        for g, e in zip(got, expected):
            assert g == e

    os.remove(outfile)
    assert not os.path.exists(outfile)


def test_CdSe_scan_95(capsys):
    fname = os.path.join(EXAMPLES_PATH, "CdSe")
    sys.argv = [sys.argv[0], fname]
    sys.argv.append("-s")
    sys.argv.append("95")
    sys.argv.append("-c")
    columns = "HerixE T_sample_LS340 HRMpzt1".split()
    sys.argv += columns

    extractSpecScan.main()
    out, _err = capsys.readouterr()
    assert isinstance(out, str)
    out = out.strip().splitlines()

    # assert out[0].startswith("program:")
    # assert out[1].startswith("read:")
    # assert out[2].startswith("wrote:")
    for item, text in enumerate("program: read: wrote:".split()):
        assert out[item].startswith(text)

    outfile = out[2][len("wrote: "):]
    assert os.path.exists(outfile)
    buf = open(outfile, "r").readlines()

    assert len(buf) == 44, "number of lines in data file"
    assert (
        "# file: " + fname == buf[0].strip()
    ), "original SPEC data file name in data file"
    assert "# scan: 95" == buf[1].strip(), "scan number in data file"
    assert "# " + "\t".join(columns) == buf[2].strip(), "column labels in data file"

    # test first and last lines of data
    # remaining lines: three columns of numbers, tab delimited
    checks = [
        # line  [expected 3 values]
        [3, [-12.063282, 297.529, 66.0]],  # first line
        [-1, [-2.0358687, 297.553, 66.0]],  # last line
    ]
    for line_number, expected in checks:
        got = list(map(float, buf[line_number].split()))
        for g, e in zip(got, expected):
            assert g == e

    os.remove(outfile)
    assert not os.path.exists(outfile)


# -----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014-2022, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
