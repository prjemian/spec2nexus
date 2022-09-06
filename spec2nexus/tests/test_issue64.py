"""Test issue 64."""

import os
import sys

from ._core import file_from_tests
from .. import extractSpecScan
from .. import spec

TESTFILE = file_from_tests("issue64_data.txt")
ARGV0 = sys.argv[0]


def test_data_file():
    assert os.path.exists(TESTFILE)

    specData = spec.SpecDataFile(TESTFILE)
    assert isinstance(specData, spec.SpecDataFile)

    scanNum = 50
    scan = specData.getScan(scanNum)
    assert isinstance(scan, spec.SpecDataFileScan)


def test_extractSpecScans_issue_64(capsys):
    args = TESTFILE + " -s 50   -c si1t  pind1"
    sys.argv = [ARGV0] + args.split() + "-G -V -Q -P".split()

    extractSpecScan.main()
    out, err = capsys.readouterr()
    out = out.splitlines()
    assert len(out) == 3, "extractSpecScan"

    for item, text in enumerate("program: read: wrote:".split()):
        assert out[item].startswith(text)

    outfile = out[2][len("wrote: "):]
    assert os.path.exists(outfile)
    os.remove(outfile)
    assert not os.path.exists(outfile)


def test_extractSpecScans_issue_66_verbose_reporting_mismatch_P_O(capsys):
    args = TESTFILE + " --verbose -s 50   -c si1t  pind1"
    sys.argv = [ARGV0] + args.split()

    extractSpecScan.main()
    out, err = capsys.readouterr()
    out = out.splitlines()

    assert len(out) == 5, "extractSpecScan"

    outfile = out[2][len("wrote: "):]
    assert os.path.exists(outfile)
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
