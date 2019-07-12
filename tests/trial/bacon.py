
"""
test of "Using Metaclasses to Create Self-Registering Plugins"

see: 

* https://www.effbot.org/zone/metaclass-plugins.htm
* https://www.pythoncentral.io/how-metaclasses-work-technically-in-python-2-and-3/
"""

from plugin_base import AutoRegister, Parent

class File(Parent, metaclass=AutoRegister):
    key = "#F"

class Date(Parent, metaclass=AutoRegister):
    key = "#D"

class Epoch(Parent, metaclass=AutoRegister):
    key = "#E"

class Comment(Parent, metaclass=AutoRegister):
    key = "#C"
