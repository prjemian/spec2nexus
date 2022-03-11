from ..control_lines import control_line_registry
from ..control_lines import ControlLines
from ._core import CONTROL_KEYS_TO_BE_TESTED


def test_one():
    assert control_line_registry is not None
    assert isinstance(control_line_registry, ControlLines)
    assert len(control_line_registry.known_keys) >= len(CONTROL_KEYS_TO_BE_TESTED)


def test_expected_keys():
    known_keys = control_line_registry.known_keys
    for key in CONTROL_KEYS_TO_BE_TESTED:
        assert key in known_keys


def test_known_keys():
    known_keys = control_line_registry.known_keys
    for key in known_keys.keys():
        assert key in CONTROL_KEYS_TO_BE_TESTED
