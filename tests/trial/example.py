
"""
test of "Using Metaclasses to Create Self-Registering Plugins"

see: 

* https://www.effbot.org/zone/metaclass-plugins.htm
* https://www.pythoncentral.io/how-metaclasses-work-technically-in-python-2-and-3/
"""

import plugins
import logging

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

logger.info("-"*40)

# loop over registered plugins
for key, cls in plugins.get_registry().items():
    if cls is not plugins.plugin_base.AutoRegister:
        obj = cls()
        logger.info(f"key={key}  class={cls}  obj={obj}")

logger.info("-"*40)
