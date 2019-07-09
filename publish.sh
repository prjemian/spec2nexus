#!/bin/bash

# publish this package

## Define the release

PACKAGE=spec2nexus
RELEASE=`python setup.py --version`
if [[ ${RELEASE} == *dirty ]] ; then
  echo "version: ${RELEASE} not ready to publish"
  exit 1
fi
## PyPI Build and upload::

python setup.py sdist bdist_wheel
twine upload dist/${PACKAGE}-${RELEASE}*

## Conda Build and upload::

### Conda channels

# if [[ ${RELEASE} == \'*\' ]]
if [[ ${RELEASE} == *rc* ]] ; then
  # anything else, such as: pre-release, release candidates, or testing purposes
  CHANNEL=aps-anl-dev
else
  # production releases
  CHANNEL=aps-anl-tag
fi

### publish (from linux)

export CONDA_BLD_PATH=/tmp/conda-bld
/bin/rm -rf ${CONDA_BLD_PATH}
/bin/mkdir -p ${CONDA_BLD_PATH}

conda build ./conda-recipe/
BUILD_DIR=${CONDA_BLD_PATH}/noarch
BUNDLE=${BUILD_DIR}/${PACKAGE}-${RELEASE}-py*_0.tar.bz2
anaconda upload -u ${CHANNEL} ${BUNDLE}

# also post to my personal channel
CHANNEL=prjemian
anaconda upload -u ${CHANNEL} ${BUNDLE}
