..
  This file describes user-visible changes between the versions.

Change History
##############

Production
**********

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
