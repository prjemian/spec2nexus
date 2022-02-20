"""Tests for the writer module."""

import h5py
import numpy
import pytest
import os

from ._core import testpath
from .. import eznx


def test_example(testpath):
    hfile = "hfile.h5"
    assert os.path.exists(testpath)
    os.chdir(testpath)

    root = eznx.makeFile(hfile, creator="eznx", default="entry")
    nxentry = eznx.makeGroup(root, "entry", "NXentry", default="data")
    eznx.write_dataset(nxentry, "title", "simple test data")
    nxdata = eznx.makeGroup(
        nxentry, "data", "NXdata", signal="counts", axes="tth", tth_indices=0,
    )
    eznx.write_dataset(nxdata, "tth", [10.0, 10.1, 10.2, 10.3], units="degrees")
    eznx.write_dataset(nxdata, "counts", [1, 50, 1000, 5], units="counts", axes="tth")
    root.close()

    """
    Test the data file for this structure::

        test.h5:NeXus data file
            @creator = eznx
            @default = 'entry'
            entry:NXentry
            @NX_class = NXentry
            @default = 'data'
            title:NX_CHAR = simple test data
            data:NXdata
                @NX_class = NXdata
                @signal = 'counts'
                @axes = 'tth'
                @axes_indices = 0
                counts:NX_INT64[4] = [1, 50, 1000, 5]
                @units = counts
                @axes = tth
                tth:NX_FLOAT64[4] = [10.0, 10.1, 10.199999999999999, 10.300000000000001]
                @units = degrees
    """
    assert os.path.exists(hfile)
    with h5py.File(hfile, "r") as hp:
        root = hp["/"]
        assert root.attrs.get("creator") == "eznx"
        assert root.attrs.get("default") == "entry"

        nxentry = root["entry"]
        assert nxentry.attrs.get("NX_class") == "NXentry"
        assert nxentry.attrs.get("default") == "data"
        assert eznx.read_nexus_field(nxentry, "title") == "simple test data"

        nxdata = nxentry["data"]
        assert nxdata.attrs.get("NX_class") == "NXdata"
        assert nxdata.attrs.get("signal") == "counts"
        assert nxdata.attrs.get("axes") == "tth"
        assert nxdata.attrs.get("tth_indices") == 0

        # test the HDF5 structure
        counts = nxdata["counts"]
        assert counts.attrs.get("units") == "counts"
        assert counts.attrs.get("axes") == "tth"
        tth = nxdata["tth"]
        assert tth.attrs.get("units") == "degrees"

        # test the data
        fields = eznx.read_nexus_group_fields(nxentry, "data", "counts tth".split())
        counts = fields["counts"]
        assert len(counts) == 4
        assert counts[2] == [1, 50, 1000, 5][2]
        tth = fields["tth"]
        assert len(tth) == 4
        assert tth[2] == [10.0, 10.1, 10.2, 10.3][2]


def test_create_dataset_None(testpath):
    hfile = "hfile.h5"
    assert os.path.exists(testpath)
    os.chdir(testpath)

    root = eznx.makeFile(hfile, creator="eznx", default="entry")
    nxentry = eznx.makeGroup(root, "entry", "NXentry", default="data")
    ds = eznx.makeDataset(nxentry, "data_is_None", None)

    with h5py.File(hfile, "r") as hp:
        root = hp["/"]
        nxentry = root["entry"]
        assert "data_is_None" in nxentry

        ds = nxentry["data_is_None"]
        value = ds[()]  # ds.value deprecated in h5py
        assert len(value) == 0
        assert isinstance(value, (bytes, str))
        assert "NOTE" in ds.attrs
        note = "no data supplied, value set to empty string"
        assert ds.attrs["NOTE"] == note


def test_write_dataset_existing(testpath):
    hfile = "hfile.h5"
    assert os.path.exists(testpath)
    os.chdir(testpath)

    root = eznx.makeFile(hfile, creator="eznx", default="entry")
    nxentry = eznx.makeGroup(root, "entry", "NXentry", default="data")
    eznx.write_dataset(nxentry, "text", "some text")
    eznx.write_dataset(nxentry, "text", "replacement text")

    with h5py.File(hfile, "r") as hp:
        root = hp["/"]
        nxentry = root["entry"]
        assert "text" in nxentry
        value = eznx.read_nexus_field(nxentry, "text", astype=str)
        assert value == "replacement text"


def test_makeExternalLink(testpath):
    hfile = "hfile.h5"
    assert os.path.exists(testpath)
    os.chdir(testpath)

    external = eznx.makeFile("external.h5", creator="eznx", default="entry")
    eznx.write_dataset(external, "text", "some text")

    root = eznx.makeFile(hfile, creator="eznx", default="entry")
    nxentry = eznx.makeGroup(root, "entry", "NXentry", default="data")
    eznx.makeExternalLink(root, "external.h5", "/text", nxentry.name + "/external_text")

    # check the external file first
    with h5py.File("external.h5", "r") as hp:
        root = hp["/"]
        assert "text" in root
        ds = root["text"]
        value = ds[()]  # ds.value deprecated in h5py
        assert value == [b"some text"]

    # check the file with the external link
    with h5py.File(hfile, "r") as hp:
        root = hp["/"]
        nxentry = root["entry"]
        assert "external_text" in nxentry
        value = eznx.read_nexus_field(nxentry, "external_text")
        assert value == "some text"
        value = eznx.read_nexus_field(nxentry, "external_text", astype=str)
        assert value == "some text"


def test_read_nexus_field_alternatives(testpath):
    hfile = "hfile.h5"
    assert os.path.exists(testpath)
    os.chdir(testpath)

    root = eznx.makeFile(hfile, creator="eznx", default="entry")
    nxentry = eznx.makeGroup(root, "entry", "NXentry", default="data")
    eznx.write_dataset(nxentry, "text", "some text")
    eznx.write_dataset(nxentry, "number", 42)
    eznx.write_dataset(nxentry, "array", [[1, 2, 3], [4, 5, 6]])

    # check the file with the external link
    with h5py.File(hfile, "r") as hp:
        root = hp["/"]
        nxentry = root["entry"]

        value = eznx.read_nexus_field(nxentry, "key_error")
        assert value is None

        value = eznx.read_nexus_field(nxentry, "text")
        assert value == "some text"
        value = eznx.read_nexus_field(nxentry, "text", astype=str)
        assert value == "some text"

        value = eznx.read_nexus_field(nxentry, "number")
        assert isinstance(value, numpy.integer)
        assert value == 42
        value = eznx.read_nexus_field(nxentry, "number", astype=float)
        assert isinstance(value, float)
        assert value == 42
        value = eznx.read_nexus_field(nxentry, "number", astype=str)
        assert isinstance(value, str)
        assert value == "42"

        ds = nxentry["array"]
        value = ds[()]  # ds.value deprecated in h5py
        expected = numpy.array([[1, 2, 3], [4, 5, 6]])
        assert (value == expected).any()

        with pytest.raises(RuntimeError) as exc:
            value = eznx.read_nexus_field(nxentry, "array")
        assert str(exc).find("unexpected 2-D data") > 0


# -----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014-2022, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
