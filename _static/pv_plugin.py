from spec2nexus.plugin_core import ControlLineBase
from spec2nexus.utils import strip_first_word

class PV_ControlLine(ControlLineBase):
    '''**#PV** -- EPICS PV associates mnemonic with PV'''
    
    key = '#PV'
    scan_attributes_defined = ['EPICS_PV']
    
    def process(self, text, spec_obj, *args, **kws):
        args = strip_first_word(text).split()
        mne = args[0]
        pv = args[1]
        if not hasattr(spec_obj, "EPICS_PV"):
            # use OrderedDict since it remembers the order we found these
            spec_obj.EPICS_PV = {}
        spec_obj.EPICS_PV[mne] = pv
