import h5py
import numpy as np
import os
import pytest

from ._core import hfile


def test_byte_str(hfile):
    assert os.path.exists(hfile)
    with h5py.File(hfile, "w") as root:
        root.create_dataset("byte_string", data=b"byte string")
        root.create_dataset("plain_string", data="plain string")
    assert os.path.exists(hfile)

    with h5py.File(hfile, "r") as root:
        assert "byte_string" in root
        for nm in "byte_string plain_string".split():
            ds = root[nm]
            assert len(ds.shape) == 0
            assert hasattr(ds, "astype")

            assert isinstance(ds[()], (bytes, str))
            assert not isinstance(ds.astype("str"), (bytes, str))
            assert not isinstance(ds.astype(ds.dtype), (bytes, str))

            v = ds[()]
            if hasattr(v, "astype"):
                assert v.astype(ds.dtype) == v


def test_array_byte_str(hfile):
    assert os.path.exists(hfile)
    with h5py.File(hfile, "w") as root:
        root.create_dataset("array_byte_string", data=b"byte string".split())
        root.create_dataset("array_plain_string", data="plain string".split())
    assert os.path.exists(hfile)

    with h5py.File(hfile, "r") as root:
        for nm in "array_byte_string array_plain_string".split():
            ds = root[nm]
            value = ds[()]
            assert not isinstance(value, (bytes, str))

            assert len(ds.shape) == 1
            assert ds.size == 2
            arr = ds[...].astype(ds.dtype)
            assert len(arr) == 2
            assert isinstance(arr, np.ndarray)


def test_scalar_float(hfile):
    assert os.path.exists(hfile)
    with h5py.File(hfile, "w") as root:
        root.create_dataset("float", data=1.2345)
        root.create_dataset("array_float", data=[0.1, 1.2345])
    assert os.path.exists(hfile)

    with h5py.File(hfile, "r") as root:
        ds = root["float"]
        assert len(ds.shape) == 0
        assert ds.size == 1
        value = ds[()]
        assert isinstance(value, float)
        assert hasattr(ds, "astype")
        assert ds[()].astype(ds.dtype) == value


def test_array_float(hfile):
    assert os.path.exists(hfile)
    with h5py.File(hfile, "w") as root:
        root.create_dataset("float", data=1.2345)
        root.create_dataset("array_float", data=[0.1, 1.2345])
    assert os.path.exists(hfile)

    with h5py.File(hfile, "r") as root:
        ds = root["array_float"]
        assert len(ds.shape) == 1
        assert ds.size == 2
        value = ds[()]
        assert isinstance(value, np.ndarray)


# -----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014-2022, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
