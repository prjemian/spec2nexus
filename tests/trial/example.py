
"""
test of "Using Metaclasses to Create Self-Registering Plugins"

see: https://www.effbot.org/zone/metaclass-plugins.htm
"""

import plugins
import logging

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

logger.info("-"*40)

# loop over registered plugins
for name, cls in plugins.get_registry().items():
    if cls is not plugins.plugin_base.Plugin:
        logger.info(f"name={name}  class={cls}")

logger.info("-"*40)
