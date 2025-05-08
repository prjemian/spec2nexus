import spec2nexus.plugin_core
import spec2nexus.spec
from spec2nexus.control_lines import control_line_registry
from spec2nexus.plugin_core import install_user_plugin

# show our plugin is not loaded
print("known: ", "#PV" in control_line_registry.known_keys) # expect False

# load our new plugin
import pathlib
install_user_plugin(pathlib.Path("pv_plugin.py").absolute())

# show that our plugin is registered
print("known: ", "#PV" in control_line_registry.known_keys) # expect True

# read a SPEC data file, scan 1
spec_data_file = spec2nexus.spec.SpecDataFile("pv_data.txt")
scan = spec_data_file.getScan(1)

# Do we have our PV data?
print(hasattr(scan, "EPICS_PV"))    # expect True
print(scan.EPICS_PV)
