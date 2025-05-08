.. _unit_testing:

Unit Testing
############

This project uses the Python *pytest* [#]_ package to apply unit testing [#]_ to
the source code.  The test code is in the ``tests/`` directories.  Various tests
have been developed starting to provide features or resolve problems reported.

The unit tests are implemented in a standard manner such that independent
review [#]_ can run the tests on this code based on the instructions provided
in ``.github/workflows`` configuration files in the project directory.

This command will run the unit tests locally::

    pytest -vvv .

Additional information may be learned with a Python package to run the tests::

    coverage run -m pytest --lf -vvv .

The *coverage* command ([#]_), will run the tests and create a report of the
percentage of the Python source code that has been executed during the unit
tests::

    coverage report --precision 3

The unit tests on GitHub automatically upload the coverage results to the
*coveralls* [#]_ site [#]_ which tracks coverage over time.

.. [#] Python *pytest* package: https://pytest.org

.. [#] unit testing: https://en.wikipedia.org/wiki/Unit_testing

.. [#] GitHub Actions workflow: https://github.com/prjemian/spec2nexus/actions

.. [#] *coverage*: https://coverage.readthedocs.io

.. [#] *coveralls*: https://coveralls.io

.. [#] *coveralls* code coverage: https://coveralls.io/github/prjemian/spec2nexus
