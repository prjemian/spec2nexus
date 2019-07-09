Installation
############

Released versions of spec2nexus are available on `PyPI 
<https://pypi.python.org/pypi/spec2nexus>`_. 

If you have ``pip`` installed, then you can install::

    $ pip install spec2nexus 

If you are using Anaconda Python and have ``conda`` installed, 
then you can install with either of these::

    $ conda install -c aps-anl-tag spec2nexus
    $ conda install -c aps-anl-dev spec2nexus
    $ conda install -c prjemian spec2nexus

Note that channel `aps-anl-tag` is for production versions
while channel `aps-anl-dev` is for development/testing versions.
The channel `prjemian` is an alternate with all versions available.

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
