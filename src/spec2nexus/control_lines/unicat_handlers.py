#!/usr/bin/env python 
# -*- coding: utf-8 -*-

'''
prjPySpec plugins for control lines defined by APS UNICAT

Handles the UNICAT control lines which write additional metadata
in the scans using #H/#V pairs of labels/values.
'''

#-----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
#-----------------------------------------------------------------------------


from spec2nexus.plugin import ControlLineHandler, strip_first_word

class UNICAT_MetadataMnemonics(ControlLineHandler):
    '''**#H** -- UNICAT metadata names (numbered rows: #H0, #H1, ...)'''

    key_regexp = '#H\d+'
    
    def process(self, text, spec_obj, *args, **kws):
        spec_obj.H.append( strip_first_word(text).split() )


class UNICAT_MetadataValues(ControlLineHandler):
    '''**#V** -- UNICAT metadata values (numbered rows: #V0, #V1, ...)'''

    key_regexp = '#V\d+'
    
    def process(self, text, spec_obj, *args, **kws):
        spec_obj.V.append( strip_first_word(text) )
        spec_obj.addPostProcessor('unicat_metadata', unicat_metadata_postprocessing)


def unicat_metadata_postprocessing(scan):
    '''
    interpret the UNICAT metadata (mostly floating point) from the scan header
    
    :param SpecDataFileScan scan: data from a single SPEC scan
    '''
    scan.metadata = {}
    for row, values in enumerate(scan.V):
        for col, val in enumerate(values.split()):
            label = scan.header.H[row][col]
            try:
                scan.metadata[label] = float(val)
            except ValueError:
                scan.metadata[label] = val
