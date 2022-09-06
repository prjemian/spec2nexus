from ..control_lines import control_line_registry
from ..plugin_core import PluginMounter
from ..plugin_core import ControlLineBase
from ..plugin_core import UNDEFINED_KEY
from ..plugin_core import install_user_plugin
from ..plugins.spec_common import SPEC_File
import pytest


def test_install_user_plugin_fails():
    with pytest.raises(FileExistsError) as exc:
        install_user_plugin("this_plugin_file_does_not_exist")
    received = str(exc.value.args[0])
    assert received == "this_plugin_file_does_not_exist"


def test_match_key():
    key = "#C"
    comment = "#C this is a SPEC comment"
    text = comment.split()[0]  # first word on the line
    plugin = control_line_registry.known_keys[key]
    assert key == plugin.key
    assert key == plugin.match_key(text)


def test_SPEC_File_Handler():
    assert not issubclass(SPEC_File, PluginMounter)
    assert issubclass(SPEC_File, ControlLineBase)
    assert SPEC_File.key in ControlLineBase.known_keys
    assert SPEC_File.key in control_line_registry.known_keys

    assert SPEC_File.key == "#F"
    key = control_line_registry.match_control_key(SPEC_File.key)
    assert key == SPEC_File.key

    plugin = control_line_registry.known_keys[key]
    assert isinstance(plugin, SPEC_File)
    assert str(plugin) == "SPEC_File(key='#F'scan_attributes_defined=[])"


def test_ControlLineBase_Handler():
    assert not issubclass(ControlLineBase, PluginMounter)
    assert hasattr(ControlLineBase, "key")
    assert hasattr(ControlLineBase, "scan_attributes_defined")
    assert ControlLineBase.key == UNDEFINED_KEY
    assert ControlLineBase.scan_attributes_defined == []

    key = control_line_registry.known_keys.get(UNDEFINED_KEY)
    assert key is None
    assert UNDEFINED_KEY not in ControlLineBase.known_keys
    assert UNDEFINED_KEY not in control_line_registry.known_keys
