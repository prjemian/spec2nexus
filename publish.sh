#!/bin/bash

# publish this package

## Define the release

PACKAGE=spec2nexus
RELEASE=`python setup.py --version`

## PyPI Build and upload::

python setup.py sdist bdist_wheel
twine upload dist/${PACKAGE}-${RELEASE}*

## Conda Build and upload::

### Conda channels

# `prjemian`    personal channel
# `aps-anl-tag` production releases
# `aps-anl-dev` anything else, such as: pre-release, release candidates, or testing purposes
CHANNEL=prjemian

### publish

CONDA_BLD_PATH=/tmp/conda-bld
/bin/rm -rf ${CONDA_BLD_PATH}
/bin/mkdir ${CONDA_BLD_PATH}

conda build ./conda-recipe/
BUILD_DIR=${CONDA_BLD_PATH}/noarch
BUNDLE=${BUILD_DIR}/${PACKAGE}-${RELEASE}-py*_0.tar.bz2
anaconda upload -u ${CHANNEL} ${BUNDLE}
