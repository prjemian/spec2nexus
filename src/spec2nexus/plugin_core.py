"""
Python plugin support for handling SPEC control lines (such as #S, #D, ...).

.. autosummary::

  ~ControlLineBase
  ~install_user_plugin

REGISTRATION SUPPORT (internal use only)

.. autosummary::

  ~PluginMounter

# from: https://gist.github.com/will-hart/5899567
# a simple Python plugin loading system
# see: http://stackoverflow.com/questions/14510286/plugin-architecture-plugin-manager-vs-inspecting-from-plugins-import
"""

import importlib
import pathlib
import re
import sys

UNDEFINED_KEY = object()


class DuplicateKeyError(KeyError):
    """Cannot add more than one plugin for the same control key."""


def install_user_plugin(plugin_file):
    """
    Install plugin(s) from a Python file.

    Potentially dangerous since this is an import of a user-created file.
    """
    plugin = pathlib.Path(plugin_file).absolute()
    if not plugin.exists():
        raise FileExistsError(plugin_file)

    # From the example in the importlib documentation:
    # https://docs.python.org/3/library/importlib.html#importing-a-source-file-directly
    spec = importlib.util.spec_from_file_location(plugin.stem, plugin)
    module = importlib.util.module_from_spec(spec)
    sys.modules[plugin.stem] = module
    spec.loader.exec_module(module)


class PluginMounter(type):
    """
    (internal) Register and initiate all plugins subclassed from PluginBase.

    .. autosummary::

       ~_enroll

    Acts as a metaclass which creates anything inheriting from PluginBase.
    A plugin mount point derived from:
    http://martyalchin.com/2008/jan/10/simple-plugin-framework/
    """

    def __init__(cls, name, bases, attrs):
        """Called when a PluginBase derived class is imported."""
        if not hasattr(cls, "plugins"):
            # Called when the metaclass is first instantiated
            cls.plugins = []
            cls.known_keys = {}
            cls.lazy_attributes = []
        else:
            # Called when a plugin class is imported
            cls._enroll(cls)

    def _enroll(cls, plugin):
        """
        Add the plugin to the plugin list and perform any registration logic.

        Expects to find these attributes:

        * ``.key`` (``str``)
        * ``.scan_attributes_defined`` (``list of str``)
        """

        # create a plugin instance and store it
        control_line_handler = plugin()

        # save the plugin reference
        cls.plugins.append(control_line_handler)
        cls.known_keys[control_line_handler.key] = control_line_handler

        for attr in control_line_handler.scan_attributes_defined:
            if attr not in cls.lazy_attributes:
                cls.lazy_attributes.append(attr)


class ControlLineBase(metaclass=PluginMounter):
    """
    Base class for SPEC data file control line handler plugins.

    Define a subclass of :class:`~spec2nexus.plugin_core.ControlLineBase` for
    each different type of control line. Refer to the supplied plugins (such as
    :mod:`spec2nexus.plugins.spec_common`) for examples. In each such class,
    it is necessary to:

    * define a string value for the ``key`` (class attribute)
    * override the definition of :meth:`process`

    As each subclass is imported, the metaclass keyword argument above
    automatically registers the plugin handler and its associated control line
    key.

    It is optional to:

    * define :meth:`postprocess`
    * define :meth:`writer`
    * define :meth:`match_key`

    PARAMETERS

    key str :
        regular expression to match a control line key, up to the first space
    scan_attributes_defined [str] :
        list of scan attributes defined in this class
    returns:
        ``None``

    .. autosummary::

       ~process
       ~postprocess
       ~writer
       ~match_key

    EXAMPLE of ``match_key`` method:

    Declaration of the ``match_key`` method is optional in a subclass.
    This is used to test a given line from a SPEC data file against the
    ``key`` of each ``ControlLineBase``.

    If this method is defined in the subclass, it will be called
    instead of :meth:`~spec2nexus.plugin.PluginManager.match_key()`.
    This is the example used by
    :class:`~spec2nexus.plugins.spec_common.SPEC_DataLine`::

        def match_key(self, text):
            try:
                float( text.strip().split()[0] )
                return True
            except ValueError:
                return False
    """

    key = UNDEFINED_KEY
    scan_attributes_defined = []

    def __str__(self):
        """String representation of this class instance."""
        return (
            f"{self.__class__.__name__}("
            f"key='{self.key}'"
            f"scan_attributes_defined={self.scan_attributes_defined}"
            ")"
        )

    def process(self, text, spec_obj, *args, **kwargs):
        """
        *required:* Handle this line from a SPEC data file.

        PARAMETERS

        text str:
            ?raw text?
        spec_obj obj:
            Instance of :class:`~spec2nexus.spec.SpecDataFile`,
            :class:`~spec2nexus.spec.SpecDataFileHeader`, or
            :class:`~spec2nexus.spec.SpecDataFileScan`
        """

        raise NotImplementedError("MUST define 'process()' method in subclass.")

    def postprocess(self, header, *args, **kws):
        """
        *optional:* More processing deferred until *after* data file has been read.
        """
        raise NotImplementedError(
            "MUST define 'postprocess()' method in subclass"
            " (if it is called in 'process()')."
        )

    def writer(self, h5parent, writer, scan, nxclass=None, *args, **kws):
        """
        *optional:* Describe how to store this data in a NeXus HDF5 file.
        """
        raise NotImplementedError(
            "MUST define 'writer()' method in subclass"
            " (if it is called in 'process()')."
        )

    def match_key(self, text):
        """
        Test if this handler's key matches text.

        :param str text: first word on the line,
            up to but not including the first whitespace
        :returns: key or None

        Applies a regular expression match using each handler's
        ``key`` as the regular expression to match with ``text``.
        """

        def _match_(text, plugin):
            """Text is first word of a line from a SPEC data file."""
            # ensure that #X and #XPCS do not both match #X
            full_pattern = "^" + plugin.key + "$"
            t = re.match(full_pattern, text)

            # test regexp match to avoid false positives
            # ensures that beginning and end are different positions
            return t and t.regs[0][1] != t.regs[0][0]

        if _match_(text, self):
            return self.key

        return None


# -----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014-2022, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------
