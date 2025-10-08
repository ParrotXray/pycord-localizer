"""
pycord-quart - A comprehensive internationalization (i18n) library for Pycord
"""

from typing import NamedTuple

from .core import I18n, t
from .types import (
    ChoiceLocalization,
    CommandLocalization,
    ContextMenuLocalization,
    Internationalization,
    Locale,
    OptionLocalization,
)


class _VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    release: str
    serial: int


__version__ = "0.1.3"
__version_info__ = _VersionInfo(0, 1, 3, "final", 0)

version = __version__
version_info = __version_info__

__all__ = (
    # Core
    "I18n",
    "t",
    # Types
    "Locale",
    "ChoiceLocalization",
    "OptionLocalization",
    "CommandLocalization",
    "ContextMenuLocalization",
    "Internationalization",
)
