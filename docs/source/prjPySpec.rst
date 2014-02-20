.. _prjPySpec:

prjPySpec
#########

Classes to read the contents of a SPEC data file.

.. index:: examples

How to use :mod:`spec2nexus.prjPySpec`
**************************************

The file **prjPySpec.py** provides Python support to read 
the scans in a SPEC data file.  (It does not provide a command-line interface.)
Here is a quick example how to use **prjPySpec.py**::

	from spec2nexus.prjPySpec import SpecDataFile
	
	specfile = SpecDataFile('data/33id_spec.dat')
	print 'SPEC file name:', specfile.specFile
	print 'SPEC file time:', specfile.headers[0].date
	print 'number of scans:', len(specfile.scans)
	
	for scanNum, scan in specfile.scans.items():
	    print scanNum, scan.scanCmd

For one example data file provided with spec2nexus, the output starts with::

	SPEC file name: samplecheck_7_17_03
	SPEC file time: Thu Jul 17 02:37:32 2003
	number of scans: 106
	1  ascan  eta 43.6355 44.0355  40 1
	2  ascan  chi 73.47 73.87  40 1
	3  ascan  del 84.6165 84.8165  20 1
	4  ascan  del 84.5199 84.7199  20 1
	5  ascan  del 84.3269 84.9269  30 1
	...
 

----

source code documentation
*************************

.. automodule:: spec2nexus.prjPySpec
    :members: 
    :synopsis: Classes to read the contents of a SPEC data file.
    