
"""
test the UXML plugin (during development)
"""

import spec2nexus.plugin
import spec2nexus.spec

# load all the supplied plugins BEFORE your custom plugins
spec2nexus.plugin.load_plugins()
registry = spec2nexus.plugin.get_registry()

# show our plugin is not loaded
print("known: ", "#UXML" in registry) # expect False

import uxml_plugin
# show that our plugin is registered
print("known: ", "#UXML" in registry) # expect True

# read a SPEC data file, scan 5
spec_data_file = spec2nexus.spec.SpecDataFile("test_1.spec")
scan = spec_data_file.getScan(1)

# Do we have our PV data?
print(hasattr(scan, "UXML"))    # expect False

# must parse full scan before our custom plugin is processed
scan.interpret()
print(hasattr(scan, "UXML"))    # expect True
print("\n".join(scan.UXML))
