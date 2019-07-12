
"""
test of "Using Metaclasses to Create Self-Registering Plugins"

see: https://www.effbot.org/zone/metaclass-plugins.htm
"""

import plugins
import plugin_base

print("-"*40)

# loop over registered plugins
for name, cls in plugin_base.registry:
    if cls is not Plugin:
        print(f"name={name}  class={cls}")

print("-"*40)
