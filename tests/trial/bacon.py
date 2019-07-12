
"""
test of "Using Metaclasses to Create Self-Registering Plugins"

see: 

* https://www.effbot.org/zone/metaclass-plugins.htm
* https://www.pythoncentral.io/how-metaclasses-work-technically-in-python-2-and-3/
"""

from plugin_base import Plugin

class BaconPlugin(metaclass=Plugin):
    pass

class FloppyBacon(metaclass=Plugin):
    pass
