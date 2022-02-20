"""Tests for the _requirements module."""

import pytest

from .. import _requirements

@pytest.mark.parametrize(
    "package", "docopt h5py lxml matplotlib numpy pyRestTable six".split()
)
def test_learn_requirements(package):
    reqs = _requirements.learn_requirements()
    assert isinstance(reqs, list)
    assert len(reqs) > 0
    assert len(reqs) == 7
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
