from spec2nexus.plugin import ControlLineHandler, strip_first_word

class XPCS_VA(ControlLineHandler):
    '''**#VA** '''

    key = '#VA\d+'

    def process(self, text, spec_obj, *args, **kws):
        if not hasattr(spec_obj, 'VA'):
            spec_obj.VA = []
            
        spec_obj.VA.append( strip_first_word(text) )
    

class XPCS_VD(ControlLineHandler):
    '''**#VD** '''

    key = '#VD\d+'

    def process(self, text, spec_obj, *args, **kws):
        if not hasattr(spec_obj, 'VD'):
            spec_obj.VD = []
            
        spec_obj.VD.append( strip_first_word(text) )
        #spec_obj.addPostProcessor('unicat_metadata', self.postprocess)
    

class XPCS_VE(ControlLineHandler):
    '''**#VE** '''

    key = '#VE\d+'

    def process(self, text, spec_obj, *args, **kws):
        if not hasattr(spec_obj, 'VE'):
            spec_obj.VE = []
            
        spec_obj.VE.append( strip_first_word(text) )
        #spec_obj.addPostProcessor('unicat_metadata', self.postprocess)
    
