from typing import Union

from discord import MessageCommand, UserCommand

from ..types import ContextMenuLocalization, Locale
from ..utils import add_localization
from .base import BaseLocalizer

__all__ = ("ContextMenuLocalizer",)


class ContextMenuLocalizer(BaseLocalizer):
    """Handles localization of MessageCommand and UserCommand objects."""

    def localize(
        self,
        command: Union[MessageCommand, UserCommand],
        locale: Locale,
        localizations: ContextMenuLocalization,
    ) -> None:
        """Apply localizations to a context menu command.

        Context menu commands only support name localization.

        Args:
            command: The context menu command to localize
            locale: The target locale
            localizations: The localization data
        """
        # Only name localization is supported for context menu commands
        if name := localizations.get("name"):
            add_localization(command, "name", locale, name)
