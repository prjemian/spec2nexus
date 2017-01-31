#!/usr/bin/env python

import os, sys, unittest
import spec2nexus
import spec2nexus.spec

path = os.path.dirname(spec2nexus.__file__)
path = os.path.abspath(os.path.join(path, 'data'))
fname = os.path.join(path, 'APS_spec_data.dat')
spec_data_file = spec2nexus.spec.SpecDataFile(fname)
print(str(spec_data_file))
assert(isinstance(spec_data_file, spec2nexus.spec.SpecDataFile))
scan = spec_data_file.getScan(2)
print(str(scan))
assert(isinstance(scan, spec2nexus.spec.SpecDataFileScan))
