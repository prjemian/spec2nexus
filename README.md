spec2nexus
==========

Converts SPEC data files and scans into NeXus HDF5 files:

    $ spec2nexus  path/to/file/specfile.dat

Writes `path/to/file/specfile.hdf5`

-   Conda install:  `conda install -c prjemian spec2nexus` (alternate)
-   Conda install:  `conda install -c aps-anl-tag spec2nexus` (production)
- Conda install:  `conda install -c aps-anl-dev spec2nexus` (development)
-   Pip install:  `pip install spec2nexus`

NOTE

spec2nexus ended development for Python 2 with release 2021.1.7, 2019-11-21.
For more information, visit https://python3statement.org/.

Provides
--------

-   **spec2nexus** : command-line tool: Convert
    [SPEC](http://certif.com) data files to
    [NeXus](http://nexusformat.org) [HDF5](http://hdfgroup.org)

-   **extractSpecScan** : command-line tool: Save columns from SPEC data
    file scan(s) to TSV files

-   **spec** : library: python binding to read SPEC data files

-   **eznx** : library: (Easy NeXus) supports writing NeXus HDF5 files
    using h5py

-   **specplot** : command-line tool: plot a SPEC scan to an image file

-   **specplot\_gallery** : command-line tool: call **specplot** for all
    scans in a list of files, makes a web gallery

Package Information
-------------------

term | description
--- | ---
**author** | Pete R. Jemian
**email** | prjemian@gmail.com
**copyright** | 2014-2022, Pete R. Jemian
**license** | Creative Commons Attribution 4.0 International Public License (see [LICENSE.txt](https://prjemian.github.io/spec2nexus/license.html) file)
**documentation** | <https://prjemian.github.io/spec2nexus/>
**source** | <https://github.com/prjemian/spec2nexus>
**PyPI** | <https://pypi.python.org/pypi/spec2nexus/>
**Release Notes** | <https://github.com/prjemian/spec2nexus/wiki/Release-Notes>
**citation** | [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3246491.svg)](https://doi.org/10.5281/zenodo.3246491)
**build badges** | ![Python Package using Conda](https://github.com/prjemian/spec2nexus/workflows/Python%20Package%20using%20Conda/badge.svg) [![image](https://coveralls.io/repos/github/prjemian/spec2nexus/badge.svg?branch=master)](https://coveralls.io/github/prjemian/spec2nexus?branch=master)    [![Total alerts](https://img.shields.io/lgtm/alerts/g/prjemian/spec2nexus.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/prjemian/spec2nexus/alerts/)   [![Codacy Badge](https://app.codacy.com/project/badge/Grade/58888d7def9e4cedb167b94c8fe53a26)](https://www.codacy.com/gh/prjemian/spec2nexus/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=prjemian/spec2nexus&amp;utm_campaign=Badge_Grade)
**release badges** | [![image](https://img.shields.io/pypi/pyversions/spec2nexus.svg)](https://pypi.python.org/pypi/spec2nexus)    [![image](https://img.shields.io/github/tag/prjemian/spec2nexus.svg)](https://github.com/prjemian/spec2nexus/tags)    [![image](https://img.shields.io/github/release/prjemian/spec2nexus.svg)](https://github.com/prjemian/spec2nexus/releases)    [![image](https://img.shields.io/pypi/v/spec2nexus.svg)](https://pypi.python.org/pypi/spec2nexus/)    [![image](https://anaconda.org/prjemian/spec2nexus/badges/version.svg)](https://anaconda.org/prjemian/spec2nexus)
