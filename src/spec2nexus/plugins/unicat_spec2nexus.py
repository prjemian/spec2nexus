#!/usr/bin/env python 
# -*- coding: utf-8 -*-

#-----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014-2016, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
#-----------------------------------------------------------------------------

'''
**#H** & **#V** - Metadata in SPEC data files as defined by APS UNICAT

Handles the UNICAT control lines which write additional metadata
in the scans using #H/#V pairs of labels/values.
'''


from spec2nexus.plugin import ControlLineHandler
from spec2nexus.utils import strip_first_word
from spec2nexus import eznx

class UNICAT_MetadataMnemonics(ControlLineHandler):
    '''
    **#H** -- UNICAT metadata names (numbered rows: #H0, #H1, ...)
    
    IN-MEMORY REPRESENTATION
    
    * (SpecDataFileHeader) : **H** : labels
    * (SpecDataFileScan): **metadata** : {labels: values}
    
    HDF5/NeXus REPRESENTATION
    
    * *NXnote* group named **metadata** below the 
      *NXentry* group, such as **/entry/metadata**
      
      * datasets created from dictionary <scan>.metadata

    '''

    key = '#H\d+'
    
    def process(self, text, spec_obj, *args, **kws):
        spec_obj.H.append( strip_first_word(text).split() )


class UNICAT_MetadataValues(ControlLineHandler):
    '''
    **#V** -- UNICAT metadata values (numbered rows: #V0, #V1, ...)
    
    IN-MEMORY REPRESENTATION
    
    * (SpecDataFileScan): **V** : values
    * (SpecDataFileScan): **metadata** : {labels: values}
    
    HDF5/NeXus REPRESENTATION
    
    * *NXnote* group named **metadata** below the 
      *NXentry* group, such as **/entry/metadata**
      
      * datasets created from dictionary <scan>.metadata

    '''

    key = '#V\d+'
    
    def process(self, text, scan, *args, **kws):
        scan.V.append( strip_first_word(text) )
        scan.addPostProcessor('unicat_metadata', self.postprocess)
    
    def postprocess(self, scan, *args, **kws):
        '''
        interpret the UNICAT metadata (mostly floating point) from the scan header
        
        :param SpecDataFileScan scan: data from a single SPEC scan (instance of SpecDataFileScan)
        '''
        scan.metadata = {}
        for row, values in enumerate(scan.V):
            for col, val in enumerate(values.split()):
                label = scan.header.H[row][col]
                try:
                    scan.metadata[label] = float(val)
                except ValueError:
                    scan.metadata[label] = val
        scan.addH5writer(self.key, self.writer)
    
    def writer(self, h5parent, writer, scan, nxclass=None, *args, **kws):
        '''Describe how to store this data in an HDF5 NeXus file'''
        if hasattr(scan, 'metadata') and len(scan.metadata) > 0:
            desc='SPEC metadata (UNICAT-style #H & #V lines)'
            group = eznx.makeGroup(h5parent, 'metadata', nxclass, description=desc)
            writer.save_dict(group, scan.metadata)
