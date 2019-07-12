
"""
test of "Using Metaclasses to Create Self-Registering Plugins"

see: https://www.effbot.org/zone/metaclass-plugins.htm
"""

import bacon
import spam

import plugin_base

def get_registry():
    return plugin_base.registry
