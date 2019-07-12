
"""
test of "Using Metaclasses to Create Self-Registering Plugins"

see: 

* https://www.effbot.org/zone/metaclass-plugins.htm
* https://www.pythoncentral.io/how-metaclasses-work-technically-in-python-2-and-3/
"""

import os
import sys
sys.path.append(os.path.join("..", "..", "src"))
import spec2nexus.plugins.apstools_specwriter_spec2nexus
import spec2nexus.plugins.fallback_spec2nexus
import spec2nexus.plugins.spec_common_spec2nexus
import spec2nexus.plugins.uim_spec2nexus
import spec2nexus.plugins.unicat_spec2nexus
import spec2nexus.plugins.XPCS_spec2nexus
import bacon
import spam

import plugin_base

def get_registry():
    return plugin_base.registry
