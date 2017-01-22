#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014-2017, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
#-----------------------------------------------------------------------------


'''
Shape scan data from raw to different dimensionality

Some SPEC macros collect data in a mesh or grid yet 
report the data as a 1-D sequence of observations.
For further processing (such as plotting), the scan data
needs to be reshaped according to its intended dimensionality.
'''
