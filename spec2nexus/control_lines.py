"""Use the plugin system to manage the SPEC control key plugins."""

__all__ = [
    "control_line_registry",
]

from .plugin_core import ControlLineBase
from .plugin_core import install_user_plugin

import pathlib


def _plugin_files():
    """Generate (a sequence of) all file names containing plugins."""
    from . import spec

    # Load packaged plugins from local files rather than listing
    # each file in the plugins_dir/__init__.py file.
    plugin_path = pathlib.Path(spec.__file__).parent / "plugins"
    yield from plugin_path.iterdir()


class ControlLines:
    """Access the installed set of control line handling plugins."""

    def __init__(self):
        for plugin_file in _plugin_files():
            if plugin_file.name.startswith("_"):
                continue
            if plugin_file.suffix not in (".py",):
                continue
            install_user_plugin(plugin_file)

    @property
    def known_keys(self):
        return ControlLineBase.known_keys

    @property
    def lazy_attributes(self):
        return ControlLineBase.lazy_attributes

    def get_control_key(self, spec_data_file_line):
        """
        Find the key that matches this line in a SPEC data file.

        Return `None` if not found.

        :param str spec_data_file_line: one line from a SPEC data file
        """
        pos = spec_data_file_line.find(" ")
        if pos < 0:
            return None
        key = spec_data_file_line[:pos]

        # try to locate the key directly
        if key in self.known_keys:
            return key

        # brute force search and match using regular expressions
        return self.match_control_key(key)

    def match_control_key(self, text):
        """
        Test if any handler's key matches text.

        :param str text: first word on the line,
            up to but not including the first whitespace
        :returns: key or None

        Applies a regular expression match using each handler's
        ``key`` as the regular expression to match with ``text``.
        """

        for key, plugin in self.known_keys.items():
            if plugin.match_key(text):
                return key

        return None

    def process(self, key, *args, **kw):
        """Pick the control line handler by key & call its ``process`` method."""
        handler = self.known_keys[key]
        if handler is not None:
            handler.process(*args, **kw)


control_line_registry = ControlLines()  # singleton

# -----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014-2022, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
