
"""
test the UXML plugin (during development)
"""

import spec2nexus.plugin
import spec2nexus.spec
import spec2nexus.writer

# load all the supplied plugins BEFORE your custom plugins
spec2nexus.plugin.load_plugins()

import uxml_plugin

spec_data_file = spec2nexus.spec.SpecDataFile("test_3.spec")

try:
    out = spec2nexus.writer.Writer(spec_data_file)
    out.save("data.hdf5", [1])
except uxml_plugin.UXML_Error as exc:
    print(str(exc))
