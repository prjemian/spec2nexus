@ECHO OFF

REM post this project to PyPI

python setup.py register sdist upload
python setup.py bdist_wheel upload
