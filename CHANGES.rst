..
  This file describes user-visible changes between the versions.

Change History
##############

Production
**********

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
