from typing import Dict, Literal, TypedDict, TypeVar, Union

from discord import ContextMenuCommand, MessageCommand, SlashCommand, UserCommand

__all__ = (
    "Locale",
    "ChoiceLocalization",
    "OptionLocalization",
    "CommandLocalization",
    "ContextMenuLocalization",
    "Internationalization",
    "Localizable",
    "CommandT",
)

# Type for all localizable commands
Localizable = Union[SlashCommand, ContextMenuCommand, MessageCommand, UserCommand]
CommandT = TypeVar("CommandT", bound=Localizable)

# Discord locale type
Locale = Literal[
    "id",
    "da",
    "de",
    "en-GB",
    "en-US",
    "es-ES",
    "es-419",
    "fr",
    "hr",
    "it",
    "lt",
    "hu",
    "nl",
    "no",
    "pl",
    "pt-BR",
    "ro",
    "fi",
    "sv-SE",
    "vi",
    "tr",
    "cs",
    "el",
    "bg",
    "ru",
    "uk",
    "hi",
    "th",
    "zh-CN",
    "ja",
    "zh-TW",
    "ko",
]


class ChoiceLocalization(TypedDict, total=False):
    """Localization for an OptionChoice.

    Maps choice values to their localized names.
    """

    name: str


class OptionLocalization(TypedDict, total=False):
    """Localization for a slash command option."""

    name: str
    description: str
    choices: Dict[str, str]  # Maps choice value to localized name


class CommandLocalization(OptionLocalization, total=False):
    """Localization for a slash command."""

    options: Dict[str, OptionLocalization]


class ContextMenuLocalization(TypedDict, total=False):
    """Localization for context menu commands (MessageCommand and UserCommand).

    Context menu commands only support name localization.
    """

    name: str


class Internationalization(TypedDict, total=False):
    """Complete internationalization structure for a locale."""

    strings: Dict[str, str]
    commands: Dict[str, CommandLocalization]
    context_menus: Dict[str, ContextMenuLocalization]
