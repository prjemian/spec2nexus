
"""
test of "Using Metaclasses to Create Self-Registering Plugins"

see: https://www.effbot.org/zone/metaclass-plugins.htm
"""

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

registry = [] # list of subclasses

class Plugin(type):
    def __init__(cls, name, bases, dict):
        logger.debug(" "*4 + "."*10)
        logger.debug(f"__init__: cls={cls}")
        logger.debug(f"__init__: name={name}")
        logger.debug(f"__init__: bases={bases}")
        logger.debug(f"__init__: dict={dict}")
        registry.append((name, cls))

    def __new__(metaname, classname, baseclasses, attrs):
        logger.debug(" "*4 + "."*10)
        logger.debug(f'__new__: metaname={metaname}')
        logger.debug(f'__new__: classname={classname}')
        logger.debug(f'__new__: baseclasses={baseclasses}')
        logger.debug(f'__new__: attrs={attrs}')
        return type.__new__(metaname, classname, baseclasses, attrs)