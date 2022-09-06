"""Unit test for XPCS plugins."""

import os
import pytest

from . import _core
from .. import spec


TEST_DATA_FILE = os.path.join(_core.EXAMPLES_PATH, "xpcs_plugin_sample.spec")


@pytest.mark.parametrize(
    "key, count",
    [
        ["VA", 2], ["VD", 1], ["VE", 2],
    ]
)
def test_key_counts(key, count):
    sd = spec.SpecDataFile(TEST_DATA_FILE)
    assert hasattr(sd.headers[0], key)

    obj = getattr(sd.headers[0], key)
    assert len(obj) == count


@pytest.mark.parametrize(
    "key, terms",
    [
        [
            "VA",
            [
                "ta1zu ta1zdo ta1zdi ta1xu ta1xd ta2zu ta2zdo ta2zdi",
                "ta2xu ta2xd motor 23 ta2rotact sa1zu sa1xu sa1zd sa1xd",
            ],
        ],
        ["VD", ["gonio1 gonio2"]],
        ["VE", ["te2xu te2xd te2y te2zu te2zdi te2zdo", "se2b se2t se2o se2i"]],
    ],
)
def test_keys(key, terms):
    sd = spec.SpecDataFile(TEST_DATA_FILE)
    assert hasattr(sd.headers[0], key)

    vobj = getattr(sd.headers[0], key)
    assert len(vobj) == len(terms)

    for i, items in enumerate(terms):
        k = "%s%d" % (key, i)
        assert k in vobj
        obj = vobj.get(k)
        assert isinstance(obj, str)
        assert obj == items


def test_XPCS_scan7():
    sd = spec.SpecDataFile(TEST_DATA_FILE)
    assert isinstance(sd, spec.SpecDataFile)

    scan = sd.getScan(7)
    assert isinstance(scan, spec.SpecDataFileScan)

    # finally, start testing the XPCS plugin
    assert "XPCS" not in scan.__dict__
    scan.interpret()  # force the plugins to be processed
    assert "XPCS" in scan.__dict__
    for key in "batch_name preset compression multi_img".split():
        assert key in scan.XPCS


# -----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014-2022, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
