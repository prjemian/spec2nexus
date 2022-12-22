..
  This file describes user-visible changes between the versions.

  subsections could include these headings (in this order), omit if no content

    Notice
    Breaking Changes
    New Features and/or Enhancements
    Fixes
    Maintenance
    Deprecations
    Contributors

Change History
##############

Production
**********

..
   2022.0.0
   +++++++++++++

   To be released 2023

2021.2.5
+++++++++++++

To be released 2022-12

Fixes
------------------

* Version number not reported correctly in certain situations (issue #299).
* Coverage/Coveralls were failing to upload code coverage results (issue #299).

Maintenance
------------------

* Add CodeQL analysis workflow, per GitHub bot recommendation (issue #295).
* Add support for Python 3.11.
* Adjust badges on root-level README page.
* When building documentation, "mock" the additional packages.
* Refactor Sphinx publishing from GitHub Action to in-line workflow.

2021.2.4
+++++++++++++

released 2022-10-14

Maintenance
------------------

* Ensure additional files are installed by conda & pip, per PEP-518.

Deprecations
------------------

* Drop support for Python <3.8.

2021.2.3
+++++++++++++

released 2022-09-19

Fixes
-----

Documentation was not published for the common plugins.

2021.2.2
+++++++++++++

released 2022-09-06

Maintenance
------------------------------------

Switch version management to setuptools-scm.

Updated Sphinx (documentation) configuration to v5.1.

2021.2.1
+++++++++++++

released 2022-05-26

New Features and/or Enhancements
------------------------------------

Added ``--output`` (short version: ``-o``) command-line option to
``spec2nexus`` application to name the output file.

Maintenance
------------------------------------

Add support for SPEC ``#R`` (user results) control line.

Contributors
------------------------------------

* Florin Boariu

2021.2.0
+++++++++++++

released 2022-03-17

Notice
------------------------------------

* Conda package now on conda-forge: ``conda install -c conda-forge spec2nexus``
* Updated format for new Change History entries.

Breaking Changes
------------------------------------

The plugin system was rebuilt to make it easier to write and load plugins,
especially custom, user-provided plugins.

New Features and/or Enhancements
------------------------------------

Added another way to access scans, using Python's slicing interface.
See the *Slice Parameters* section for more details and examples.

Add new diffractometer configuration reports:

* ``str(scan.diffractometer)``:  minimal view of ``scan``
* ``scan.diffractometer.print_brief(scan)`` : content similar to SPEC's ``wh``
* ``scan.diffractometer.print_all(scan)`` : content similar to SPEC's ``pa``

Documentation reorganized and using new Furo theme.

New documentation of the NeXus file structure.

Fixes
------------------------------------

* ``eznx``: needs to return text as ``str`` (not ``bytes``).
* ``twoc``: diffractometer geometry has 2-D lattice and reflection(s)

Maintenance
------------------------------------

* Optimize initial load times for data files.
* Code tests now use real examples of non-zero MCA data using files with both
  single and multiple MCA detectors.
* Tests of code using Python 3.7, 3.8, 3.9, 3.10
* All unit test code now in-source using ``pytest``
* Code is now compliant with `PEP8 <https://pep8.org/>`_ (Python code style guide).
* Increase number of unit tests to improve code coverage (now ~95%).
* Resume use of test code coverage reporting:
  https://coveralls.io/github/prjemian/spec2nexus

Deprecations
------------------------------------

* Python versions lower than 3.7 are no longer supported.

Contributors
------------------------------------

* Radu Abrudan

-------------

Older Releases
+++++++++++++++

:2021.1.11: released *2022.02.24*

   * re-release due to documentation publishing workflow problem

:2021.1.10: released *2022.02.24*

   * re-release due to documentation publishing workflow problem

:2021.1.9: released *2022.02.24*

    * `#239 <https://github.com/prjemian/spec2nexus/issues/239>`_
       publish documentation at https://prjemian.github.io/spec2nexus/

:2021.1.8: released *2020.11.10*

    * `#221 <https://github.com/prjemian/spec2nexus/issues/221>`_
       move CI from travis-ci to Github Actions, test with python 3.8
    * `#217 <https://github.com/prjemian/spec2nexus/issues/217>`_
       raise ValueError when ``#L`` and ``#N`` lines do not agree

.. note:: Python 2 end of support

   spec2nexus stopped development for Python 2 after release *2021.1.7*, *2019-11-21*.
   For more information, visit https://python3statement.org/.

:2021.1.7: released *2019-11-21*

    Note: Last version with support for Python 2

    * `#213 <https://github.com/prjemian/spec2nexus/issues/213>`_
       copy data file to gallery

    * `#208 <https://github.com/prjemian/spec2nexus/issues/208>`_
       add more diagnostics to gallery web page comments

    * `#191 <https://github.com/prjemian/spec2nexus/issues/191>`_
       write each positioner to NXpositioner group

    * `#188 <https://github.com/prjemian/spec2nexus/issues/188>`_
       catenate continued lines before parsing data

    * `#186 <https://github.com/prjemian/spec2nexus/issues/186>`_
       remove unused code

:2021.1.6: released *2019.11.01*

    * `#210 <https://github.com/prjemian/spec2nexus/issues/210>`_
       add `-c prjemian` conda channel

:2021.1.5: released *2019.11.01*

    * `#209 <https://github.com/prjemian/spec2nexus/issues/209>`_
       *pyRestTable* added to installation requirements

:2021.1.4: released *2019.10.18*

    * `#206 <https://github.com/prjemian/spec2nexus/issues/206>`_
       specplot_gallery: replot shows all existing plots

:2021.1.3: released *2019.08.19* - only update plots with *new* content

    * `#202 <https://github.com/prjemian/spec2nexus/issues/202>`_
       specplot_gallery: switch to SVG (from PNG) for plots
    * `#201 <https://github.com/prjemian/spec2nexus/issues/201>`_
       spec: subsequent calls to read() duplicate scans -- FIXED
    * `#126 <https://github.com/prjemian/spec2nexus/issues/126>`_
       spec: new ``update_available`` property
    * `#108 <https://github.com/prjemian/spec2nexus/issues/108>`_
       specplot_gallery: only update plots with *new* content

:2021.1.2: released *2019.08.15*, plugin enhancements

    * `#197 <https://github.com/prjemian/spec2nexus/issues/197>`_
       plugins: handle empty empty #O0 or #P0 list
    * `#195 <https://github.com/prjemian/spec2nexus/issues/195>`_
       drop CII badge: not useful to spec2nexus
    * `#190 <https://github.com/prjemian/spec2nexus/issues/190>`_
       writer: link content into NXinstrument group
    * `#51 <https://github.com/prjemian/spec2nexus/issues/51>`_
       plugins: interpret #Gn control lines

:2021.1.1: released *2019.07.22*, refactor

    * `#181 <https://github.com/prjemian/spec2nexus/issues/181>`_
       plugins: revised technique to load control line handlers

:2021.1.0: released *2019.07.15*, new features

    **NEW**

    * support for ``#UXML`` metadata
    * support for ``hklscan`` scans
    * improved support for ``mesh`` and ``hklmesh`` scans

    * `#159 <https://github.com/prjemian/spec2nexus/issues/159>`_
       handle #UXML metadata control lines
    * `#155 <https://github.com/prjemian/spec2nexus/issues/155>`_
       module: writer - recognize hklscan
    * `#150 <https://github.com/prjemian/spec2nexus/issues/150>`_
       module: writer - increase coverage of unit tests: mesh, hklmesh
    * `#148 <https://github.com/prjemian/spec2nexus/issues/148>`_
       module: eznx - increase coverage of unit tests

:2021.0.1: released *2019.07.13*, plugin loading and documentation

    * `#170 <https://github.com/prjemian/spec2nexus/issues/170>`_
       describe how to write & load Control Line Handler plugins
    * `#169 <https://github.com/prjemian/spec2nexus/issues/169>`_
       announce deprecation of python 2
    * `#165 <https://github.com/prjemian/spec2nexus/issues/165>`_
       resolve conda build error
    * `#149 <https://github.com/prjemian/spec2nexus/issues/149>`_
       unit tests: ``units`` module

:2021.0.0: released *2019.07.12*, API change affecting plugins

    **API change**:
    Changed how plugins are defined and registered.
    Custom plugins must be modified and import code revised
    to work with new system.

    * `#168 <https://github.com/prjemian/spec2nexus/pull/168>`_
       plugins are now self-registering
    * `#166 <https://github.com/prjemian/spec2nexus/issues/166>`_
       fix conda packaging

:2020.0.2: released *2019.07.09*, bug fixes and code review suggestions

    NOTE: conda package is broken (no plugins directory).
    Only use ``pip install spec2nexus`` with this release.

    * `#164 <https://github.com/prjemian/spec2nexus/issues/164>`_
       post conda packages to `aps-anl-tag` channel
    * `#161 <https://github.com/prjemian/spec2nexus/issues/161>`_
       read files with no #E control line
    * `#156 <https://github.com/prjemian/spec2nexus/issues/156>`_
       LGTM code review
    * `#153 <https://github.com/prjemian/spec2nexus/issues/153>`_
       LGTM code review

:2020.0.0: released *2019.05.16*, major release

    * `#145 <https://github.com/prjemian/spec2nexus/issues/145>`_
       unit tests for header content
    * `#144 <https://github.com/prjemian/spec2nexus/issues/144>`_
       eznx `makeDataset()` now recognizes if data is `ndarray`
    * `#123 <https://github.com/prjemian/spec2nexus/issues/123>`_
       Accept data files with no header control lines (#F #E #D #C sequence)
    * `#113 <https://github.com/prjemian/spec2nexus/issues/113>`_
       unit tests for eznx
    * `#70 <https://github.com/prjemian/spec2nexus/issues/70>`_
       remove h5toText, find this now in `punx` package

:2019.0503.0: released *2019.05.03*, tag

    * `#142 <https://github.com/prjemian/spec2nexus/issues/142>`_
       DuplicateSpecScanNumber with multiple #F sections
    * `#137 <https://github.com/prjemian/spec2nexus/issues/137>`_
       (again) bug in #U control line handling

:2019.0501.0: released *2019.05.01*, tag

    * `#137 <https://github.com/prjemian/spec2nexus/issues/137>`_
       bug in #U control line handling
    * `#140 <https://github.com/prjemian/spec2nexus/issues/140>`_
       change: #U data goes into `<object>.U` list (name changed from `UserReserved`)

:2.1.0: 2019.04.26, release

    * `#135 <https://github.com/prjemian/spec2nexus/issues/135>`_
       switch to semantic versioning
    * `#133 <https://github.com/prjemian/spec2nexus/issues/133>`_
       support user control line "#U " with plugin
    * `#131 <https://github.com/prjemian/spec2nexus/issues/131>`_
       support #MD control lines from apstools.SpecWriterCallback
    * `#125 <https://github.com/prjemian/spec2nexus/issues/125>`_
       fluorescence spectra in files for RSM3D
    * `#120 <https://github.com/prjemian/spec2nexus/issues/120>`_
       do not mock `six` package in documentation
    * `#119 <https://github.com/prjemian/spec2nexus/issues/119>`_
       delimiters in #H/#V lines with or without text values
    * `#116 <https://github.com/prjemian/spec2nexus/issues/116>`_
       process data from spock

	see [release notes](https://github.com/prjemian/spec2nexus/wiki/releasenotes__2-1-0)

	It takes a couple steps to upgrade an existing conda installation from version 2017.nnnn to newer version 2.1.0

	- add a declaration of `spec2nexus < 2000` in the `conda-meta/pinned` file in the conda environment
	- `conda update -c prjemian spec2nexus` (should change to 2.1.0)

	It may still be necessary to uninstall and reinstall spec2nexus to effect an update:

		conda uninstall -y spec2nexus
		conda install -c prjemian spec2nexus

:2019.0422.0: (tag only)

    * tag as-is, for issue #131

:2019.0321.0: (tag only)

    * tag as-is, post conda noarch package and post to pypi

:2017.901.4:

    * `#62 <https://github.com/prjemian/spec2nexus/issues/62>`_
       support Python3
    * `#112 <https://github.com/prjemian/spec2nexus/issues/112>`_
       merge py3-62 branch
    * `#111 <https://github.com/prjemian/spec2nexus/issues/111>`_
       Change raise statements to use parens around arguments. Affects issue #62
    * `#114 <https://github.com/prjemian/spec2nexus/issues/114>`_
       travis-ci for python 3.5 & 3.6
    * `#107 <https://github.com/prjemian/spec2nexus/issues/107>`_
       Problems accessing SpecDataFileScan.data
    * `#95 <https://github.com/prjemian/spec2nexus/issues/95>`_
       document final release steps


:2017.711.0:

    * `#110 <https://github.com/prjemian/spec2nexus/issues/110>`_
       Ownership of info between #L/data & #S n
    * `#109 <https://github.com/prjemian/spec2nexus/issues/109>`_
      Spaces in data labels on `#L` and other lines

:2017.522.1:

    * `#105 <https://github.com/prjemian/spec2nexus/issues/105>`_
      ignore extra content in `#@CALIB` control lines
    * `#104 <https://github.com/prjemian/spec2nexus/issues/104>`_
      use versioneer (again)
    * `#101 <https://github.com/prjemian/spec2nexus/issues/101>`_
       documentation URL & date/time added to every gallery page
    * `#100 <https://github.com/prjemian/spec2nexus/issues/100>`_
      conda package installs properly on Windows now
    * `#99 <https://github.com/prjemian/spec2nexus/issues/99>`_
      BUG: specplot_gallery: plots of hklscan from file `lmn40.spe`
    * `#98 <https://github.com/prjemian/spec2nexus/issues/98>`_
      BUG: specplot_gallery: identify as directory not found
    * `#52 <https://github.com/prjemian/spec2nexus/issues/52>`_
      remove deprecated *prjPySpec* code

:2017.317.0:

   * minor update of the *2017.3.0* release

:2017.3.0:

    * `#103 <https://github.com/prjemian/spec2nexus/issues/103>`_
      changed *converters* back to *utils*
    * `#97 <https://github.com/prjemian/spec2nexus/issues/97>`_
      PyPI project description now formatted properly
    * `#90 <https://github.com/prjemian/spec2nexus/issues/90>`_
      use *versioneer* (again)

:2017-0202.0:

    * `#99 <https://github.com/prjemian/spec2nexus/issues/99>`_
      fix list index error in *hklscan* when hkl are all constant

    * `#96 <https://github.com/prjemian/spec2nexus/issues/96>`_
      combine steps when publishing to PyPI

:2017-0201.0:

    * `milestone punch list <https://github.com/prjemian/spec2nexus/milestone/3?closed=1>`_

    * `#73 <https://github.com/prjemian/spec2nexus/issues/73>`_
      refactor mesh and MCA data parsing code

    * `#67 <https://github.com/prjemian/spec2nexus/issues/67>`_
      apply continuous integration via travis-ci

    * `#66 <https://github.com/prjemian/spec2nexus/issues/66>`_
      add verbosity option

    * `#65 <https://github.com/prjemian/spec2nexus/issues/65>`_
      apply unit testing

    * `#64 <https://github.com/prjemian/spec2nexus/issues/64>`_
      *extractSpecScan*: fixed list index out of range

    * `#63 <https://github.com/prjemian/spec2nexus/issues/63>`_
      *extractSpecScan*: command line option to select range of scans

    * `#56 <https://github.com/prjemian/spec2nexus/issues/56>`_
      *specplot* and *specplot_gallery*: add from USAXS instrument and generalize

:2016.1025.0: standardize the versioning kit with pyRestTable and pvWebMonitor
:2016.1004.0:

    * `#61 <https://github.com/prjemian/spec2nexus/issues/61>`_
      release info from git (dropped versioneer package)

:2016.0829.0:

    * `#60 <https://github.com/prjemian/spec2nexus/issues/60>`_
      Add new plugin test for XPCS plugin (thanks to John Hammonds)

:2016.0615.1:

    * `#57 <https://github.com/prjemian/spec2nexus/issues/57>`_
      keep information from unrecognized control lines,

    * `#56 <https://github.com/prjemian/spec2nexus/issues/56>`_
      add *specplot* support,

    * `#55 <https://github.com/prjemian/spec2nexus/issues/55>`_
      accept arbitrary number of MCA spectra

:2016.0601.0: match complete keys, use unix EOL internally, do not fail if no metadata
:2016.0216.0:

    * `#36 <https://github.com/prjemian/spec2nexus/issues/36>`_
      identify NIAC2014-compliant NeXus files

:2016.0210.0: bugfix: eznx.makeGroup() now correctly sets attributes on new group + documentation for NIAC2014 attributes
:2016.0204.0:

    * `#45 <https://github.com/prjemian/spec2nexus/issues/45>`_
      handle case when no data points in scan ,

    * `#46 <https://github.com/prjemian/spec2nexus/issues/46>`_
      spec.getScan() ensures argument is used as ``str``

:2016.0201.0: added spec.getScanNumbersChronological(), spec.getFirstScanNumber(), and spec.getLastScanNumber()
:2016.0131.0:

    * `#43 <https://github.com/prjemian/spec2nexus/issues/43>`_
      support new NeXus method for default/signal/axes/_indices,

:2016.0130.0: fixed `#44 <https://github.com/prjemian/spec2nexus/issues/44>`_
:2015.1221.1:

    * `#40 <https://github.com/prjemian/spec2nexus/issues/40>`_
      added versioneer support

:2015.1221.0:

    * `#39 <https://github.com/prjemian/spec2nexus/issues/39>`_
      read scans with repeated scan numbers

:2015.0822.0: extractSpecScan: add option to report scan heading data, such as positioners and Q
:2015.0214.0: h5toText: handle HDF5 'O' data type (variable length strings)
:2015.0127.0: spec: ignore bad data lines
:2015.0125.0: spec: change handling of #L & #X, refactor detection of scanNum and scanCmd
:2015.0113.0: dropped requirement of *lxml* package
:2014.1228.1: spec: build mne:name cross-references for counters and positioners
:2014.1228.0: show version in documentation
:2014.1028.0: spec: quietly ignore unrecognized scan content *for now*
:2014.1027.1: spec: major changes in SPEC file support: **custom plugins**

    * **spec** based on plugins for each control line, users can add plugins
    * declared **prjPySpec** module as legacy, code is frozen at *2014.0623.0* release
    * added **spec** module to replace **prjPySpec**

:2014.0623.0: updated argparse settings
:2014.0622.2: added extractSpecScan.py to the suite from the USAXS project
:2014.0410.0: restore scan.fileName variable to keep interface the same for some legacy clients
:2014.0404.1: fix sdist utf8 problem, see: http://bugs.python.org/issue11638
:2014.0404.0: tree_api_parser moved back into NeXpy project
:2014.0320.6: handle multiple header sections in SPEC data file
:2014.0320.5: fix the new project URL
:2014.0320.4: Sphinx cannot build PDF with code-block in a footnote
:2014.0320.3: note the new home URL in the packaging, too, drop nexpy requirement, default docs theme
:2014.0320.2: tree_api_parse will go back into nexpy project, remove docs of it here
:2014.0320.1: allow readthedocs to build Sphinx without extra package requirements
:2014.0320.0:

    * new home page at http://spec2nexus.readthedocs.org, easier to publish there
    * move common methods from __init__.py so docs will build at readthedocs.org
    * new test case fails existing SPEC reader, ignore blank lines

:2014.03.11: documentation
:2014.03.09: h5toText: option to suppress printing of attributes, put URLs in command-line usage documentation, better test of is_spec_file()
:2014.03.08: fixed string writer and content display bug in eznx, added h5toText.py, prjPySpec docs improved again
:2014.03.051: prjPySpec now handles SPEC v6 data file header additions, add new getScanCommands() method
:2014.03.04: (2014_Mardi_Gras release) removed nexpy project requirement from setup, prjPySpec raises exceptions now
:2014.03.02: drops nexus tree API (and its dependencies) in favor of native h5py writer

Development: GitHub repository
******************************

:2014.02.20: version number fits PEP440, LICENSE file included in sdist, more documentation and examples
:2014-02-19: reference published documentation (re-posted)
:2014-02-19: add documentation framework
:2014-02-18: fork to GitHub to make generally available

Development: NeXpy branch
*************************

:2014-01: briefly, a branch in https://github.com/nexpy/nexpy

  * spec2nexus added during this phase
  * relies on nexpy.api.nexus for NeXus support

Production: USAXS livedata
**************************

:2010-2014: production use

  * support livedata WWW page of APS USAXS instrument

    * (http://usaxs.xray.aps.anl.gov/livedata/),

  * https://subversion.xray.aps.anl.gov/trac/small_angle/browser/USAXS/livedata/prjPySpec.py
  * converted from Tcl

:2000-2010: Tcl code (*readSpecData.tcl*) in production use at APS sectors 32, 33, & 34
