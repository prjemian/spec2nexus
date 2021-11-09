import os
import pytest
import shutil
import tempfile


_ppath = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
EXAMPLES_DIR = os.path.join(_ppath, "data")
PLUGINS_DIR = os.path.join(_ppath, "plugins")
TEST_DATA_DIR = os.path.abspath(os.path.join(_ppath, "..", "..", "tests", "data"))


@pytest.fixture
def testdir():
    # setUp
    owd = os.getcwd()
    tempdir = tempfile.mkdtemp()
    os.chdir(tempdir)
    yield tempdir

    # tearDown
    if os.path.exists(owd):
        os.chdir(owd)
    if os.path.exists(tempdir):
        shutil.rmtree(tempdir, ignore_errors=True)


@pytest.fixture(scope="function")
def hfile():
    tfile = tempfile.NamedTemporaryFile(suffix=".hdf5", delete=False)
    tfile.close()
    hfile = tfile.name
    yield hfile

    if os.path.exists(hfile):
        os.remove(hfile)


# @pytest.fixture(scope="function")
# def sfile():
#     tfile = tempfile.NamedTemporaryFile(suffix=".spec", delete=False)
#     tfile.close()
#     sfile = tfile.name
#     yield sfile

#     if os.path.exists(sfile):
#         os.remove(sfile)


@pytest.fixture(scope="function")
def tempdir():
    path = tempfile.mkdtemp()
    yield path

    if os.path.exists(path):
        shutil.rmtree(path, ignore_errors=True)
