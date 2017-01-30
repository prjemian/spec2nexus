.. _unit_testing:

Unit Testing
############

Since release 2017.0201.0, this project relies on the Python *unittest* [#]_ 
package to apply
unit testing [#]_ to the source code.  The test code is in the `tests`
directory.  Various tests have been developed starting with the *2017.0201.0* 
release to provide features or resolve problems reported.  The tests are not 
yet exhaustive yet the reported code coverage [#]_ is well over 80%.

The unit tests are implemented in a standard manner such that independent
review [#]_ can run the tests on this code based on the instructions provided 
in a `.travis.yml` configuration file in the project directory.

This command will run the unit tests locally::

    python tests

Additional information may be learned with a Python package to run the tests::

    coverage run -a tests && coverage report -m

The *coverage* command ([#]_), will run the tests and then prepare a report of 
the percentage of the Python source code that has been executed during the
unit tests.

.. note:: The number of lines reported by *coverage* may differ from that 
   reported by *travis-ci*.  The primary reason is that certain tests involving
   access to information from GitHub may succeed or not depending on the 
   "Github API rate limit". [#]_

.. [#] Python *unittest* package: 
   https://docs.python.org/2/library/unittest.html

.. [#] unit testing: https://en.wikipedia.org/wiki/Unit_testing

.. [#] *coveralls* code coverage: https://coveralls.io/github/prjemian/spec2nexus

.. [#] *travis-ci* continuous intregration: https://travis-ci.org/prjemian/spec2nexus

.. [#] *coverage*: https://coverage.readthedocs.io

.. [#] Github API rate limit: https://developer.github.com/v3/rate_limit/
