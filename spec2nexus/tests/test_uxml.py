"""Tests for the UXML control lines."""


from . import _core
from ._core import file_from_tests
from ._core import hfile
from .. import writer
from ..plugins import uxml
from ..spec import SpecDataFile, SpecDataFileScan

from lxml import etree
import h5py
import numpy
import os
import pytest


SPEC_DATA_FILE_LINES = """
#UXML <group name="attenuator1" NX_class="NXattenuator" number="1" pv_prefix="33idd:filter:Fi1:" unique_id="33idd:filter:Fi1:">
#UXML   <dataset name="enable" unique_id="find_me">Enable</dataset>
#UXML   <hardlink name="found_you" target_id="find_me"/>
#UXML   <dataset name="lock">Lock</dataset>
#UXML   <dataset name="type">Ti</dataset>
#UXML   <dataset name="thickness" type="float" units="micron">251.000</dataset>
#UXML   <dataset name="attenuator_transmission" type="float">3.55764458e-02</dataset>
#UXML   <dataset name="status">Out</dataset>
#UXML </group>
"""


def test_process():
    """test the :meth:`process` method"""
    scan = SpecDataFileScan(None, "")
    assert isinstance(scan, SpecDataFileScan)

    # test create instance
    handler = uxml.UXML_metadata()
    assert isinstance(handler, uxml.UXML_metadata)

    # test that specific attributes not yet defined
    txt = "this is text"
    assert not hasattr(scan, "UXML")
    assert "UXML_metadata" not in scan.postprocessors

    # test that specific attributes now defined
    handler.process("#UXML " + txt, scan)
    assert hasattr(scan, "UXML")
    assert "UXML_metadata" in scan.postprocessors
    assert scan.postprocessors["UXML_metadata"] == handler.postprocess
    assert isinstance(scan.UXML, list)
    assert scan.UXML == [txt]


def test_parse():
    """test that UXML lines are parsed"""

    scan = SpecDataFileScan(None, "")
    handler = uxml.UXML_metadata()
    for line in SPEC_DATA_FILE_LINES.strip().splitlines():
        txt = line.strip()
        if len(txt) > 0:
            handler.process(txt, scan)
    assert hasattr(scan, "UXML")
    # print ('\n'.join([ '%3d: %s' % (i,j) for i,j in enumerate(scan.UXML) ]))
    assert 9 == len(scan.UXML)
    assert hasattr(scan, "h5writers")
    assert "UXML_metadata" not in scan.h5writers
    assert not hasattr(scan, "UXML_root")


def test_postprocess():
    """test the :meth:`postprocess` method"""
    scan = SpecDataFileScan(None, "")
    handler = uxml.UXML_metadata()
    for line in SPEC_DATA_FILE_LINES.strip().splitlines():
        txt = line.strip()
        if len(txt) > 0:
            handler.process(txt, scan)

    handler.postprocess(scan)
    assert "UXML_metadata" in scan.h5writers
    assert hasattr(scan, "UXML_root")
    root = scan.UXML_root
    assert not isinstance(root, str)
    assert isinstance(root, etree._Element)
    assert "UXML" == root.tag
    node = root[0]
    assert "group" == node.tag
    assert "attenuator1" == node.get("name")
    assert "NXattenuator" == node.get("NX_class")
    assert 7 == len(node)
    node = node[0]
    assert "dataset" == node.tag
    assert "enable" == node.get("name")
    assert "find_me" == node.get("unique_id")


def test_writer():
    """test the :meth:`writer` method"""
    scan = SpecDataFileScan(None, "")
    handler = uxml.UXML_metadata()
    for line in SPEC_DATA_FILE_LINES.strip().splitlines():
        txt = line.strip()
        if len(txt) > 0:
            handler.process(txt, scan)
    handler.postprocess(scan)

    assert hasattr(scan, "UXML_root"), "need to test writer()"
    root = scan.UXML_root
    schema_file = os.path.join(_core.PLUGINS_PATH, "uxml.xsd")
    assert os.path.exists(schema_file)
    schema_doc = etree.parse(schema_file)
    schema = etree.XMLSchema(schema_doc)
    result = schema.validate(root)
    assert result


def test_UXML_DocumentInvalid():
    spec_file = file_from_tests("test_3_error.spec")
    assert os.path.exists(spec_file)

    spec_data = SpecDataFile(spec_file)
    assert isinstance(spec_data, SpecDataFile)

    scan = spec_data.getScan(1)

    with pytest.raises(etree.DocumentInvalid) as exc:
        scan.interpret()
    received = str(exc.value.args[0])
    expected = "Element 'group': Character content other than whitespace is not allowed"
    assert received.startswith(expected), (received, exc)


def test_file_3(hfile):
    spec_file = file_from_tests("test_3.spec")
    assert os.path.exists(spec_file)

    spec_data = SpecDataFile(spec_file)
    assert isinstance(spec_data, SpecDataFile)
    out = writer.Writer(spec_data)
    out.save(hfile, [1, ])

    # text that UXML group defined as expected
    assert os.path.exists(hfile)
    with h5py.File(hfile, "r") as h5_file:
        assert "S1" in h5_file
        nxentry = h5_file["/S1"]
        assert "UXML" in nxentry
        uxml = nxentry["UXML"]
        assert "NX_class" in uxml.attrs
        assert uxml.attrs["NX_class"] == "NXnote"

        # spot-check a couple items
        # group: attenuator_set
        assert "attenuator_set" in uxml
        group = uxml["attenuator_set"]
        prefix = group.attrs.get("prefix")
        description = group.attrs.get("description")
        unique_id = group.attrs.get("unique_id")
        assert prefix == "33idd:filter:"
        assert description == "33-ID-D Filters"
        assert unique_id is None

        # <dataset name="corrdet_counter">corrdet</dataset>
        assert "corrdet_counter" in group
        ds = group["corrdet_counter"]
        # https://docs.h5py.org/en/stable/whatsnew/2.1.html?highlight=dataset#dataset-value-property-is-now-deprecated
        value = ds[()]
        assert value == [b"corrdet"]

        # <dataset name="wait_time" type="float" units="s">0.500</dataset>
        assert "wait_time" in group
        ds = group["wait_time"]
        assert ds.attrs.get("units") == "s"
        value = ds[()]  # ds.value deprecated in h5py
        assert value == numpy.array([0.5])

        # <hardlink name="attenuator1" target_id="33idd:filter:Fi1:"/>
        assert "attenuator1" in group
        attenuator1 = group["attenuator1"]
        target = attenuator1.attrs.get("target")
        assert target != attenuator1.name
        assert target == uxml["attenuator1"].name

        addr = "/S1/UXML/ad_file_info/file_format"
        assert addr in h5_file
        ds = h5_file[addr]
        value = ds[()]  # ds.value deprecated in h5py
        assert value == [b"TIFF"]


def test_file_4(hfile):
    spec_file = file_from_tests("test_4.spec")
    assert os.path.exists(spec_file)

    spec_data = SpecDataFile(spec_file)
    assert isinstance(spec_data, SpecDataFile)
    out = writer.Writer(spec_data)
    out.save(hfile, [1, ])

    # the ONLY structural difference between test_3.spec
    # and test_4.spec is the presence of this hardlink
    assert os.path.exists(hfile)
    with h5py.File(hfile, "r") as h5_file:
        source = h5_file["/S1/UXML/ad_detector/beam_center_x"]
        link = h5_file["/S1/UXML/beam_center_x"]
        target = source.attrs.get("target")

        assert source.name != link.name
        assert target is not None
        assert target == source.name
        assert target == link.attrs.get("target")


# -----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014-2022, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
