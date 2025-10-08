from typing import Dict

from discord import MISSING, Option, OptionChoice

from ..types import Locale

__all__ = ("ChoiceLocalizer",)


class ChoiceLocalizer:
    """Handles localization of OptionChoice objects."""

    @staticmethod
    def localize_choices(
        option: Option,
        locale: Locale,
        choice_localizations: Dict[str, str],
    ) -> None:
        """Localize choices within an option.

        Args:
            option: The option containing choices to localize
            locale: The target locale
            choice_localizations: Dict mapping choice value to localized name
        """
        if not hasattr(option, "choices") or not option.choices:
            return

        for choice in option.choices:
            if isinstance(choice, OptionChoice):
                # Check if this choice value has a localization
                localized_name = choice_localizations.get(str(choice.value))
                if localized_name:
                    ChoiceLocalizer._add_choice_localization(choice, locale, localized_name)

    @staticmethod
    def _add_choice_localization(
        choice: OptionChoice,
        locale: Locale,
        localized_name: str,
    ) -> None:
        """Add name localization to an OptionChoice.

        Args:
            choice: The choice to localize
            locale: The target locale
            localized_name: The localized name for this choice
        """
        if choice.name_localizations in (None, MISSING):
            choice.name_localizations = {locale: localized_name}
        else:
            choice.name_localizations[locale] = localized_name
