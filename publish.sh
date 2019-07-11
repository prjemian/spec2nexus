#!/bin/bash

# publish this package

## Define the release

PACKAGE=`python setup.py --name`
RELEASE=`python setup.py --version`
echo "PACKAGE: ${PACKAGE}"
echo "RELEASE: ${RELEASE}"

if [[ ${RELEASE} == *dirty || ${RELEASE} == *+* ]] ; then
  echo "version: ${RELEASE} not ready to publish"
  exit 1
fi

## PyPI Build and upload::

echo "Building for upload to PyPI"
python setup.py sdist bdist_wheel
twine upload dist/${PACKAGE}-${RELEASE}*

## Conda Build and upload::

### Conda channels

if [[ ${RELEASE} == *rc* ]] ; then
  # anything else, such as: pre-release, release candidates, or testing purposes
  CHANNEL=aps-anl-dev
else
  # production releases
  CHANNEL=aps-anl-tag
fi

### publish (from linux)

echo "Building for upload to conda"

export CONDA_BLD_PATH=/tmp/conda-bld
/bin/mkdir -p ${CONDA_BLD_PATH}

export LOG_FILE=${CONDA_BLD_PATH}/${PACKAGE}-${RELEASE}-conda-build.log
conda build ./conda-recipe/ 2>&1 | tee ${LOG_FILE}

echo "upload to conda CHANNEL: ${CHANNEL}"
_package_=$(echo ${PACKAGE} | tr '[:upper:]' '[:lower:]')
BUNDLE=${CONDA_BLD_PATH}/noarch/${_package_}-${RELEASE}-*_0.tar.bz2
anaconda upload -u ${CHANNEL} ${BUNDLE}

# also post to my personal channel
anaconda upload ${BUNDLE}
