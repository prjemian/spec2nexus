from spec2nexus.plugin import ControlLineHandler, strip_first_word
from spec2nexus.eznx import makeGroup
from spec2nexus.spec import SpecDataFileHeader

class XPCS_VA(ControlLineHandler):
    '''**#VA**'''

    key = '#VA\d+'

    def process(self, text, spec_obj, *args, **kws):
        subkey = text.split()[0].lstrip('#')
        if not hasattr(spec_obj, 'VA'):
            spec_obj.VA = {}
        spec_obj.VA[subkey] = strip_first_word(text)
        if isinstance(spec_obj, SpecDataFileHeader):
            spec_obj.addH5writer(self.key, self.writer)
    
    def writer(self, h5parent, writer, scan, nxclass=None, *args, **kws):
        ''' Describe how to write VA data'''
        desc = "XPCS VA parameters"
        group = makeGroup(h5parent, 'VA', nxclass,description=desc)
        dd = {}
        for item, value in scan.VA.items():
            dd[item] = map(str, value.split())
        writer.save_dict(group, dd)

class XPCS_VD(ControlLineHandler):
    '''**#VD** '''

    key = '#VD\d+'

    def process(self, text, spec_obj, *args, **kws):
        subkey = text.split()[0].lstrip('#')
        if not hasattr(spec_obj, 'VD'):
            spec_obj.VD = {}
            
        spec_obj.VD[subkey] = strip_first_word(text)
        if isinstance(spec_obj, SpecDataFileHeader):
            spec_obj.addH5writer(self.key, self.writer)
    
    def writer(self, h5parent, writer, scan, nxclass=None, *args, **kws):
        ''' Describe how to write VD data'''
        desc = "XPCS VD parameters"
        group = makeGroup(h5parent, 'VD', nxclass, description=desc)
        dd = {}
        for item, value in scan.VD.items():
            dd[item] = map(str, value.split())
        writer.save_dict(group, dd)

class XPCS_VE(ControlLineHandler):
    '''**#VE** '''

    key = '#VE\d+'

    def process(self, text, spec_obj, *args, **kws):
        subkey = text.split()[0].lstrip('#')
        if not hasattr(spec_obj, 'VE'):
            spec_obj.VE = {}
            
        spec_obj.VE[subkey] = strip_first_word(text)
        if isinstance(spec_obj, SpecDataFileHeader):
            spec_obj.addH5writer(self.key, self.writer)
    
    def writer(self, h5parent, writer, scan, nxclass=None, *args, **kws):
        ''' Describe how to write VE data'''
        desc = "XPCS VE parameters"
        group = makeGroup(h5parent, 'VE', nxclass,description=desc)
        dd = {}
        for item, value in scan.VE.items():
            dd[item] = map(str, value.split())
        writer.save_dict(group, dd)
