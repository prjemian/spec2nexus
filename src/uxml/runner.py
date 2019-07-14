
"""
test the UXML plugin (during development)
"""

import spec2nexus.plugin
import spec2nexus.spec
import spec2nexus.writer

# load all the supplied plugins BEFORE your custom plugins
spec2nexus.plugin.load_plugins()

import uxml_plugin       # lgtm

test_file = "test_4.spec"
output_file = "data.hdf5"
spec_data_file = spec2nexus.spec.SpecDataFile(test_file)

try:
    out = spec2nexus.writer.Writer(spec_data_file)
    out.save(output_file, [1])
except uxml_plugin.UXML_Error as exc:
    print(str(exc))
