"""Tests for scanf module."""

import pytest

from ..scanf import scanf


@pytest.mark.parametrize("degc_sp", [21.1, 20])
def test_temperature_numbers(degc_sp):
    fmt = "#X %gKohm (%gC)"

    t_sp = 273.15 + degc_sp
    cmd = fmt % (degc_sp, t_sp)
    result = scanf(fmt, cmd)
    assert result is not None
    assert len(result) == 2
    a, b = result
    assert degc_sp == a
    assert t_sp == b


@pytest.mark.parametrize(
    "expected, fmt, arg",
    [
        ((123.456e-1,), "%g", "123.456e-1"),
        ((123.456,), "%f", "123.456e-1"),
        ((20,), "%g", "20"),
        ((0,), "%g", "0."),
        ((0,), "%g", ".0"),
        ((0,), "%g", ".0e-21"),
        (None, "%g", "."),
    ],
)
def test_battery(fmt, arg, expected):
    assert scanf(fmt, arg) == expected


# -----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014-2022, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
