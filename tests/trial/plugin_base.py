
"""
test of "Using Metaclasses to Create Self-Registering Plugins"

see: 

* https://www.effbot.org/zone/metaclass-plugins.htm
* https://www.pythoncentral.io/how-metaclasses-work-technically-in-python-2-and-3/
"""

import logging
logger = logging.getLogger(__name__)


class PluginError(RuntimeError): ...
class PluginKeyNotDefined(PluginError): ...
class PluginDuplicateKeyError(PluginError): ...
class PluginBadKeyError(PluginError): ...


registry = {} # dictionary of known Plugin subclasses


def register_plugin(cls):
    obj = cls()

    if not hasattr(obj, "key") or obj.key is None:
        emsg = f"'key' not defined: {obj.__class__}"
        raise PluginKeyNotDefined(emsg)

    key = obj.key

    if key in registry:
        emsg = f"duplicate key={key}: {obj.__class__}"
        previous = registry[key]()
        emsg += f", previously defined: {previous.__class__}"
        raise PluginDuplicateKeyError(emsg)
    
    if len(key.strip().split()) != 1:
        emsg = f"badly-formed 'key': received '{key}'"
        raise PluginBadKeyError(emsg)

    registry[key] = cls


class AutoRegister(type):
    __key__ = None
    def __init__(cls, name, bases, dict):
        logger.debug(" "*4 + "."*10)
        logger.debug(f"__init__: cls={cls}")
        logger.debug(f"__init__: name={name}")
        logger.debug(f"__init__: bases={bases}")
        logger.debug(f"__init__: dict={dict}")
        register_plugin(cls)

    def __new__(metaname, classname, baseclasses, attrs):
        logger.debug(" "*4 + "."*10)
        logger.debug(f'__new__: metaname={metaname}')
        logger.debug(f'__new__: classname={classname}')
        logger.debug(f'__new__: baseclasses={baseclasses}')
        logger.debug(f'__new__: attrs={attrs}')
        return type.__new__(metaname, classname, baseclasses, attrs)


class Parent:
    key = None
    def __str__(self):
        return(f"{self.__class__.__name__}(key='{self.key}')")
    def do_this(self):
        print(self.__class__.__name__)
