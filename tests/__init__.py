
#-----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014-2017, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
#-----------------------------------------------------------------------------

# advice: http://stackoverflow.com/questions/191673/preferred-python-unit-testing-framework?rq=1
# advice: http://stackoverflow.com/questions/17001010/how-to-run-unittest-discover-from-python-setup-py-test#21726329
# advice: http://stackoverflow.com/questions/6164004/python-package-structure-setup-py-for-running-unit-tests?noredirect=1&lq=1


import os
import unittest
import sys

_path = os.path.join(os.path.dirname(__file__), '..',)
if _path not in sys.path:
    sys.path.insert(0, _path)


def suite(*args, **kw):
    from tests import _version_test
    from tests import data_03_06_JanTest
    from tests import test_extractSpecScan
    from tests import test_plugin
    from tests import test_scanf
    from tests import test_spec
    from tests import test_specplot
    from tests import test_specplot_gallery
    from tests import test_writer
    from tests import test_XPCSplugin
    from tests import issue64
    test_suite = unittest.TestSuite()
    test_list = [
        _version_test,
        data_03_06_JanTest,
        test_extractSpecScan,
        test_plugin,
        test_scanf,
        test_spec,
        test_specplot,
        test_specplot_gallery,
        test_writer,
        test_XPCSplugin,
        issue64,
        ]

    for test in test_list:
        test_suite.addTest(test.suite())
    return test_suite


if __name__ == '__main__':
    runner=unittest.TextTestRunner(verbosity=2)
    runner.run(suite())
