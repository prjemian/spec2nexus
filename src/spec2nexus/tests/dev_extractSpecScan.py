"""developer test for extractSpecScan"""

import os
import pytest
import shutil
import sys

from . import _core
from ._core import testpath
from .. import extractSpecScan
ARGV0 = sys.argv[0]


# args = 'data/APS_spec_data.dat -s 1 6   -c mr USAXS_PD I0 seconds'
# args = 'data/33id_spec.dat     -s 1 6   -c H K L signal elastic I0 seconds'
# args = 'data/CdOsO     -s 1 1.1 48   -c HerixE H K L T_control_LS340  T_sample_LS340 ICO-C  PIN-D  PIN-C Seconds'
# args = 'data/02_03_setup.dat     -s 46  1-3   -c ar  ay  dy  Epoch  seconds  I0  USAXS_PD'
# args = 'data/02_03_setup.dat     -s 47   -c mr seconds  I0  USAXS_PD'
args = "../src/spec2nexus/data/xpcs_plugin_sample.spec  -s 7   -c img_n  Epoch  ccdc"


@pytest.mark.parametrize(
    "filename, options",
    [
        ["APS_spec_data.dat", "-s 1 6   -c mr USAXS_PD I0 seconds"],
        ["33id_spec.dat", "-s 1 6   -c H K L signal elastic I0 seconds"],
        ["CdOsO", "-s 1 1.1 48   -c HerixE H K L T_control_LS340  T_sample_LS340 ICO-C  PIN-D  PIN-C Seconds"],
        ["02_03_setup.dat", "-s 46  1-3   -c ar  ay  dy  Epoch  seconds  I0  USAXS_PD"],
        ["02_03_setup.dat", "-s 47   -c mr seconds  I0  USAXS_PD"],
        ["xpcs_plugin_sample.spec", "-s 7   -c img_n  Epoch  ccdc"],
    ]
)
def test_developer_testing(filename, options, testpath):
    assert os.path.exists(testpath)
    assert os.getcwd() == testpath

    starting_file = os.path.join(_core.EXAMPLES_PATH, filename)
    assert os.path.exists(starting_file)

    spec_file = os.path.join(testpath, "specdata.dat")
    shutil.copy(starting_file, spec_file)
    assert os.path.exists(spec_file)

    sys.argv = [ARGV0, spec_file]
    sys.argv += options.split()
    sys.argv += "-G -V -Q -P".split()
    extractSpecScan.main()
    assert len(os.listdir(testpath)) > 1

# -----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014-2022, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
