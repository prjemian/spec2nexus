"""
Test issue #216.

Index error reading a single scan SPEC file.

The output file gets created but only contains /S1/definition,
running spec2nexus-2021.1.7.

This data file has problems which were not identified clearly
until this issue.  All problems are related to incorrect formatting
of the `#L` line.  The number of columns specified in #N matches
the number of values on each data line (7).

1. The number of columns specified in #N does not match the number
   of columns described in #L
2. The labels given on #L are only delimited by single spaces.
   This results in only one label defined.
3. The number of separate labels given in #L (6) does not equal the
   number of data columns.
"""

import os
import pytest

from ._core import file_from_tests
from .. import spec


TEST_SPEC_FILE = file_from_tests("issue216_scan1.spec")


def test_nexus_file():
    assert os.path.exists(TEST_SPEC_FILE)

    sdf = spec.SpecDataFile(TEST_SPEC_FILE)
    assert isinstance(sdf, spec.SpecDataFile)

    scanNum = 1
    scan = sdf.getScan(scanNum)
    assert isinstance(scan, spec.SpecDataFileScan)

    # force plugins to process (& raise ValueError)
    with pytest.raises(ValueError):
        scan.interpret()


# -----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014-2022, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
