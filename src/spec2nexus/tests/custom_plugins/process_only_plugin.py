from spec2nexus.plugin_core import ControlLineBase
from spec2nexus.utils import strip_first_word


class MyControlLinePlugin(ControlLineBase):
    """**#TEST** -- custom control line handler"""

    key = "#TEST"
    scan_attributes_defined = ["MyTest"]

    def process(self, text, spec_obj, *args, **kws):
        s = strip_first_word(text)
        if not hasattr(spec_obj, "MyTest"):
            # a list allows for more than one #TEST in a scan
            spec_obj.MyTest = []
        spec_obj.MyTest.append(s)
