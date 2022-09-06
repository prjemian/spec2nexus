"""Test issue 123."""

import os
import sys

from . import _core
from .. import spec


ARGV0 = sys.argv[0]


def test_spock_file():
    spec_file = os.path.join(_core.EXAMPLES_PATH, "spec_from_spock.spc")
    assert os.path.exists(spec_file)
    assert not spec.is_spec_file_with_header(spec_file)
    assert spec.is_spec_file(spec_file)

    sdf = spec.SpecDataFile(spec_file)
    assert isinstance(sdf, spec.SpecDataFile)
    assert len(sdf.headers) == 1, "expected number of headers"

    header = sdf.headers[0]
    assert isinstance(header, spec.SpecDataFileHeader)
    assert len(header.raw) == 0, "no raw content"
    assert len(header.date) != 0, "default date"
    assert header.epoch == 1505468350, "default epoch"
    assert len(header.comments) == 0, "expected number of header comments"
    assert len(header.O) == 0, "defined positioner label rows"
    assert len(header.H) == 0, "defined metadata label rows"

    scans = sdf.getScanNumbers()
    assert len(scans) == 171, "expected number of scans"

    scan = sdf.getScan(2)
    assert isinstance(scan, spec.SpecDataFileScan)

    assert len(scan.P) == 20, "defined positioner value rows"
    assert len(header.O) == 20, "defined positioner label rows"
    assert scan.header.O == header.O, "same object"
    assert len(scan.V) == 0, "defined metadata value rows"
    assert len(scan.L) == 23, "defined data column labels"
    assert len(scan.data) == 23, "defined data variables"
    assert scan.L[0] == "Pt_No", "first data column label"
    assert scan.L[-1] == "dt", "last data column label"

    d1 = scan.data.get("Pt_No")
    assert d1 is not None, "data 'Pt_No' exists"
    assert len(d1) == 51, "data 'Pt_No' has expected number of values"
    assert scan.scanCmd == "dscan th -0.5 0.5 50 1.0", "scan command"
    assert scan.scanNum == "2", "scan number as string"
    assert scan.scanNum != 2, "scan number as integer"
    assert len(scan.positioner) == 155, "defined positioners"

    d1 = scan.positioner.get("abs")
    assert d1 is not None, "positioner 'abs' exists"
    assert d1 == 0.0, "positioner 'abs' value is zero"


def test_33id_file():
    spec_file = os.path.join(_core.EXAMPLES_PATH, "33id_spec.dat")
    assert os.path.exists(spec_file)
    assert spec.is_spec_file_with_header(spec_file)
    assert spec.is_spec_file(spec_file)

    sdf = spec.SpecDataFile(spec_file)
    assert isinstance(sdf, spec.SpecDataFile)

    scans = sdf.getScanNumbers()
    assert len(scans) == 106, "expected number of scans"
    assert len(sdf.headers) == 1, "expected number of headers"

    header = sdf.headers[0]
    assert isinstance(header, spec.SpecDataFileHeader)
    assert len(header.raw) > 0, "raw content"
    assert len(header.date) > 0, "defined date"
    assert header.epoch == 1058427452, "expected epoch"
    assert len(header.comments) == 1, "expected number of header comments"
    assert len(header.O) == 4, "defined positioner label rows"
    assert len(header.H) == 21, "defined metadata label rows"


# -----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014-2022, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
