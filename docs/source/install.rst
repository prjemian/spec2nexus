Installation
############

Released versions of spec2nexus are available on `PyPI 
<https://pypi.python.org/pypi/spec2nexus>`_. 

If you have ``pip`` installed, then you can install::

    $ pip install spec2nexus 

If you are using Anaconda Python and have ``conda`` installed, then you can install::

    $ conda install -c http://conda.anaconda.org/prjemian spec2nexus

..  build the conda kit *after* pushing a new update to PyPI
    use conda skeleton pypi::

    cd /tmp
    mkdir conda
    cd conda
    conda skeleton pypi spec2nexus
    conda build spec2nexus
    conda convert --platform all /local/Apps/anaconda/conda-bld/linux-64/spec2nexus-2016.0601.0-py27_0.tar.bz2 -o /tmp/conda
    
    jemian@gov /tmp/conda $ ll -R *-*
		linux-32:
		total 5.8M
		-rw-r--r-- 1 jemian aesbc 5.8M Jun  1 15:12 spec2nexus-2016.0601.0-py27_0.tar.bz2
		
		linux-64:
		total 5.8M
		-rw-r--r-- 1 jemian aesbc 5.8M Jun  1 15:12 spec2nexus-2016.0601.0-py27_0.tar.bz2
		
		osx-64:
		total 5.8M
		-rw-r--r-- 1 jemian aesbc 5.8M Jun  1 15:11 spec2nexus-2016.0601.0-py27_0.tar.bz2
		
		win-32:
		total 5.8M
		-rw-r--r-- 1 jemian aesbc 5.8M Jun  1 15:12 spec2nexus-2016.0601.0-py27_0.tar.bz2
		
		win-64:
		total 5.8M
		-rw-r--r-- 1 jemian aesbc 5.8M Jun  1 15:12 spec2nexus-2016.0601.0-py27_0.tar.bz2
	jemian@gov /tmp/conda $ 
    

The latest development versions of spec2nexus can be downloaded from the
GitHub repository listed above::

    $ git clone http://github.com/prjemian/spec2nexus.git

To install in the standard Python location::

    $ cd spec2nexus
    $ python setup.py install

To install in user's home directory::

    $ python setup.py install --user

To install in an alternate location::

    $ python setup.py install --prefix=/path/to/installation/dir

Required Libraries
##################

These libraries are required to write NeXus data files.
They are not required to read SPEC data files.

=============  =============================
Library        URL
=============  =============================
h5py           http://www.h5py.org
numpy          http://numpy.scipy.org/
=============  =============================

Optional Libraries
##################

These libraries are used by the :ref:`specplot <specplot>`
and  :ref:`specplot_gallery <specplot_gallery>` modules
of the *spec2nexus* package but are not required
just to read SPEC data files or write NeXus data files.

=============  =============================
Library        URL
=============  =============================
MatPlotLib     http://matplotlib.org/
=============  =============================
