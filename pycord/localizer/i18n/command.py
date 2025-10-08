from discord import SlashCommand, utils

from ..types import CommandLocalization, Locale
from ..utils import add_localization
from .base import BaseLocalizer
from .choice import ChoiceLocalizer

__all__ = ("CommandLocalizer",)


class CommandLocalizer(BaseLocalizer):
    """Handles localization of SlashCommand objects."""

    def localize(
        self,
        command: SlashCommand,
        locale: Locale,
        localizations: CommandLocalization,
    ) -> None:
        """Apply localizations to a slash command.

        Args:
            command: The slash command to localize
            locale: The target locale
            localizations: The localization data
        """
        # Localize command name
        if name := localizations.get("name"):
            add_localization(command, "name", locale, name)

        # Localize command description
        if description := localizations.get("description"):
            add_localization(command, "description", locale, description)

        # Localize options
        if options := localizations.get("options"):
            self._localize_options(command, locale, options)

    def _localize_options(
        self,
        command: SlashCommand,
        locale: Locale,
        options_localizations: dict,
    ) -> None:
        """Localize command options.

        Args:
            command: The slash command containing options
            locale: The target locale
            options_localizations: Dict mapping option names to their localizations
        """
        for option_name, localization in options_localizations.items():
            option = utils.get(command.options, name=option_name)
            if not option:
                continue

            # Localize option name
            if op_name := localization.get("name"):
                add_localization(option, "name", locale, op_name)

            # Localize option description
            if op_description := localization.get("description"):
                add_localization(option, "description", locale, op_description)

            # Localize option choices
            if op_choices := localization.get("choices"):
                ChoiceLocalizer.localize_choices(option, locale, op_choices)
