from abc import ABC, abstractmethod
from typing import Dict, Union

from ..types import (
    CommandLocalization,
    ContextMenuLocalization,
    Locale,
    Localizable,
)

__all__ = ("BaseLocalizer",)


class BaseLocalizer(ABC):
    """Abstract base class for all localizers."""

    @abstractmethod
    def localize(
        self,
        command: Localizable,
        locale: Locale,
        localizations: Union[CommandLocalization, ContextMenuLocalization, Dict],
    ) -> None:
        """Apply localizations to a command.

        Args:
            command: The command to localize
            locale: The target locale
            localizations: The localization data
        """
        pass
