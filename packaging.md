# Packaging Hints

## Define Release

    RELEASE=2020.0.0

## PyPI upload

Preceed the wildcard with tag text (`spec2nexus-${RELEASE}*`)::

	python setup.py sdist bdist_wheel
	twine upload dist/spec2nexus-${RELEASE}*

## Conda upload

In the upload command below, use the text reported 
at (near) the end of a successful conda build.

	conda build ./conda-recipe/
	anaconda upload /home/mintadmin/Apps/anaconda/conda-bld/noarch/spec2nexus-${RELEASE}-py*_0.tar.bz2
