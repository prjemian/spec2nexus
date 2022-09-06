"""Test issue 128."""

import os
import pytest

from . import _core
from .. import spec


TEST_SPEC_FILE = os.path.join(_core.EXAMPLES_PATH, "CdOsO")


def test_data_file():
    assert os.path.exists(TEST_SPEC_FILE)

    sdf = spec.SpecDataFile(TEST_SPEC_FILE)
    assert isinstance(sdf, spec.SpecDataFile)

    with pytest.raises(ValueError):
        # #128 failed due to assumption of int keys
        sorted(sdf.scans.keys(), key=int)

    # next line assumes #128 is fixed
    scans = sdf.getScanNumbers()
    assert len(scans) == 74, "expected number of scans"
    assert "1" in scans
    assert "1.1" in scans


# -----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014-2022, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
