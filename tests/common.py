'''
common code for unit testing of spec2nexus
'''


import os
import sys
from six import StringIO



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
