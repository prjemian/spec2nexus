import spec2nexus.plugin
import spec2nexus.spec

# call get_plugin_manager() BEFORE you import any custom plugins
manager = spec2nexus.plugin.get_plugin_manager()

# show our plugin is not loaded
print("known: ", "#PV" in manager.registry) # expect False

import pv_plugin
# show that our plugin is registered
print("known: ", "#PV" in manager.registry) # expect True

# read a SPEC data file, scan 1
spec_data_file = spec2nexus.spec.SpecDataFile("pv_data.txt")
scan = spec_data_file.getScan(1)

# Do we have our PV data?
print(hasattr(scan, "EPICS_PV"))    # expect True
print(scan.EPICS_PV)
