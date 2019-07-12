
"""
test of "Using Metaclasses to Create Self-Registering Plugins"

see: https://www.effbot.org/zone/metaclass-plugins.htm
"""

registry = [] # list of subclasses

class Plugin(type):
    def __init__(cls, name, bases, dict):
        print(" "*4 + "."*10)
        print(f"__init__: cls={cls}")
        print(f"__init__: name={name}")
        print(f"__init__: bases={bases}")
        print(f"__init__: dict={dict}")
        registry.append((name, cls))

    def __new__(metaname, classname, baseclasses, attrs):
        print(" "*4 + "."*10)
        print(f'__new__: metaname={metaname}')
        print(f'__new__: classname={classname}')
        print(f'__new__: baseclasses={baseclasses}')
        print(f'__new__: attrs={attrs}')
        return type.__new__(metaname, classname, baseclasses, attrs)