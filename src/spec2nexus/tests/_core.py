import os
import pytest
import shutil
import tempfile

from ..spec import UNRECOGNIZED_KEY

# parent (package source code) directory
_ppath = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# tests directory
_tpath = os.path.dirname(__file__)
EXAMPLES_PATH = os.path.join(_ppath, "data")
PLUGINS_PATH = os.path.join(_ppath, "plugins")
TEST_DATA_PATH = os.path.abspath(os.path.join(_tpath, "data"))

CONTROL_KEYS_TO_BE_TESTED = set([
    UNRECOGNIZED_KEY,
    "@A\\d*",
    "#@[cC][aA][lL][iI][bB]",
    "#@CHANN",
    "#@CTIME",
    "#@MCA",
    "#@ROI",
    "#C",
    "#CCD",
    "#D",
    "#E",
    "#F",
    "#G\\d+",
    "#H\\d+",
    "#I",
    "#j\\d+",
    "#J\\d+",
    "#L",
    "#M",
    "#MD\\w*",
    "#N",
    "#o\\d+",
    "#O\\d+",
    "#P\\d+",
    "#Q",
    "#R",
    "#S",
    "#T",
    "#U",
    "#UIM\\w*",
    "#UXML",
    "#V\\d+",
    "#VA\\d+",
    "#VD\\d+",
    "#VE\\d+",
    "#X",
    "#XPCS",
    "scan_data",
])


@pytest.fixture
def testpath():
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


def file_from_examples(fname):  # rename to file_from_examples
    return os.path.join(EXAMPLES_PATH, fname)


def file_from_tests(fname):
    return os.path.join(TEST_DATA_PATH, fname)


def getActiveSpecDataFile(path):
    """Simulate a SPEC data file in-use for data acquisition."""
    assert os.path.exists(path)
    spec_data_file = os.path.join(path, "specdata.txt")
    assert not os.path.exists(spec_data_file)

    starting_file = os.path.join(TEST_DATA_PATH, "refresh1.txt")
    assert os.path.exists(starting_file)
    shutil.copy(starting_file, spec_data_file)
    return spec_data_file


def addMoreScans(spec_data_file, more_file="refresh2.txt"):
    """Simulate addition of scans to active SPEC data file."""
    more_content_file = os.path.join(TEST_DATA_PATH, more_file)
    with open(more_content_file, "r") as fp:
        more_scans = fp.read()
    with open(spec_data_file, "a") as fp:
        fp.write(more_scans)


# -----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014-2022, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
