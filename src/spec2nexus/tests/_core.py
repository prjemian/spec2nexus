import os
import pytest
import shutil
import tempfile


_ppath = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


@pytest.fixture(scope="function")
def hfile():
    tfile = tempfile.NamedTemporaryFile(suffix=".hdf5", delete=False)
    tfile.close()
    hfile = tfile.name
    yield hfile

    if os.path.exists(hfile):
        os.remove(hfile)


@pytest.fixture(scope="function")
def tempdir():
    path = tempfile.mkdtemp()
    yield path

    if os.path.exists(path):
        shutil.rmtree(path, ignore_errors=True)
