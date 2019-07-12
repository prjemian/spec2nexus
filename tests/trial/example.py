
"""
test of "Using Metaclasses to Create Self-Registering Plugins"

see: https://www.effbot.org/zone/metaclass-plugins.htm
"""

import plugins

print("-"*40)

# loop over registered plugins
for name, cls in plugins.get_registry():
    if cls is not plugins.plugin_base.Plugin:
        print(f"name={name}  class={cls}")

print("-"*40)
