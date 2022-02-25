"""Tests for the _requirements module."""

import pytest

from .. import _requirements

EXPECTED_PACKAGES = "h5py lxml matplotlib-base numpy".split()


@pytest.mark.parametrize("package", EXPECTED_PACKAGES)
def test_learn_requirements(package):
    reqs = _requirements.learn_requirements()
    assert isinstance(reqs, list)
    assert len(reqs) > 0
    assert len(reqs) == len(EXPECTED_PACKAGES)
    assert package in reqs


# -----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014-2022, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
