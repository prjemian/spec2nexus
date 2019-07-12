
"""
test of "Using Metaclasses to Create Self-Registering Plugins"

see: 

* https://www.effbot.org/zone/metaclass-plugins.htm
* https://www.pythoncentral.io/how-metaclasses-work-technically-in-python-2-and-3/
"""

from plugin_base import Plugin

class File(metaclass=Plugin):
    key = "#F"

class Date(metaclass=Plugin):
    key = "#D"

class Epoch(metaclass=Plugin):
    key = "#E"

class Comment(metaclass=Plugin):
    key = "#C"
