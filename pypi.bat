@ECHO OFF

REM post this project to PyPI

python setup.py register sdist bdist_wheel upload
