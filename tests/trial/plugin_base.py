
"""
test of "Using Metaclasses to Create Self-Registering Plugins"

see: https://www.effbot.org/zone/metaclass-plugins.htm
"""

registry = [] # list of subclasses

class Plugin(object):
    class __metaclass__(type):
        def __init__(cls, name, bases, dict):
            type.__init__(name, bases, dict)
            registry.append((name, cls))
            print(f"registered name={name}  class={cls}")
