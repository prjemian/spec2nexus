import numpy
import pytest

from ._core import hfile
from .. import utils


def test_clean_name():
    candidate = "0 is not a good name"
    result = utils.clean_name(candidate)
    assert candidate != result
    expected = "_0_is_not_a_good_name"
    assert expected == result

    candidate = "entry_5"
    result = utils.clean_name(candidate)
    assert candidate == result


def test_iso8601():
    expected = "2010-11-03T13:39:34"
    spec = utils.iso8601("Wed Nov 03 13:39:34 2010")
    assert spec == expected

    expected = "2017-09-15T04:39:10"
    spock = utils.iso8601("09/15/17 04:39:10")
    assert spock == expected


def test_split_columns():
    expected = ["two theta", "motor x", "scint counter"]
    spec = utils.split_column_labels("two theta  motor x  scint counter")
    assert spec == expected


def test_sanitize_name():
    # legacy support only
    expected = "_0_is_not_a_good_name"
    spec = utils.sanitize_name(None, "0 is not a good name")
    assert spec == expected


def test_reshape_data():
    arr = numpy.array([0, 1, 2, 3, 4, 5])
    expected = [[0, 1], [2, 3], [4, 5]]
    spec = utils.reshape_data(arr, (3, 2))
    assert (spec == expected).all()

    expected = [[0, 1, 2], [3, 4, 5]]
    spec = utils.reshape_data(arr, (2, 3))
    assert (spec == expected).all()


@pytest.mark.parametrize(
    "key, expected",
    [
        ["0", (0, 0)],
        ["0.", (0, 0)],
        ["0.0", (0, 0)],
        ["5.2", (5, 2)],
        ["11.10", (11, 10)],
    ]
)
def test_split_scan_number_string(key, expected):
    assert utils.split_scan_number_string(key) == expected


# -----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014-2022, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
