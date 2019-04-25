'''
common code for unit testing of spec2nexus
'''

#-----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014-2019, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
#-----------------------------------------------------------------------------

import h5py
import os
from six import StringIO
import sys
import tempfile


def create_test_file(content_function=None, suffix='.hdf5'):
    """
    create a new (HDF5) test file
    
    :param obj content_function: method to add content(s) to hdf5root
    """
    hfile = tempfile.NamedTemporaryFile(suffix=suffix, delete=False)
    hfile.close()
    if suffix == '.hdf5':
        hdf5root = h5py.File(hfile.name, "w")
        if content_function is not None:
            content_function(hdf5root)
        hdf5root.close()
    return str(hfile.name)


class Capture_stdout(list):
    '''
    capture all printed output (to stdout) into list
    
    example::
    
        with tests.common.Capture_stdout() as printed_lines:
            do_something_that_prints_to_stdout()
        do_somthing_with_output(printed_lines)
        
    # http://stackoverflow.com/questions/16571150/how-to-capture-stdout-output-from-a-python-function-call
    '''
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout
