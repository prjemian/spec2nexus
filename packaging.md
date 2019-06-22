# Packaging Hints

## Define Release

    RELEASE=`python ./setup.py version | grep "^Version: " | cut -d' ' -f2`
    # next line will show if ANY changes since tag
    echo ${RELEASE} | grep +

## PyPI upload

Preceed the wildcard with tag text (`spec2nexus-${RELEASE}*`)::

	python setup.py sdist bdist_wheel
	twine upload dist/spec2nexus-${RELEASE}*

## Conda upload

In the upload command below, use the text reported 
at (near) the end of a successful conda build.

	conda build ./conda-recipe/
	anaconda upload /home/mintadmin/Apps/anaconda/conda-bld/noarch/spec2nexus-${RELEASE}-py*_0.tar.bz2
