from typing import Dict

from discord import ApplicationContext, Bot, MessageCommand, SlashCommand, UserCommand, utils

from .i18n import CommandLocalizer, ContextMenuLocalizer
from .types import (
    CommandLocalization,
    CommandT,
    ContextMenuLocalization,
    Internationalization,
    Locale,
)
from .utils import normalize_locale

__all__ = ("I18n", "_")


class I18n:
    """A class for internationalization.

    Parameters
    ----------
    bot: discord.Bot
        The pycord bot to add internationalization for.
    consider_user_locale: bool
        Whether to consider the user's locale when translating responses.
        By default this is `False` and responses will be based on the server's locale.
    **translations:
        Key-value pairs of locales and translations based on the `Internationalization` TypedDict.

    Attributes
    ----------
    instance: I18n
        The initialized I18n instance.
    current_locale: Locale
        The locale of the last invocation.
    translations: Dict[Locale, Dict[str, str]]
        String translations. Accessed via `I18n.get_text`.
    localizations: Dict[Locale, Dict[str, CommandLocalization]]
        Command localizations. Applied via `.localize` or `.localize_commands`.
    context_menu_localizations: Dict[Locale, Dict[str, ContextMenuLocalization]]
        Context menu command localizations.
    """

    instance: "I18n"
    current_locale: Locale

    def __init__(
        self,
        bot: Bot,
        *,
        consider_user_locale: bool = False,
        **internalizations: Internationalization,
    ) -> None:
        self.bot: Bot = bot
        self.consider_user_locale = consider_user_locale

        # Initialize localizers
        self.command_localizer = CommandLocalizer()
        self.context_menu_localizer = ContextMenuLocalizer()

        # Parse translations
        self.translations: Dict[Locale, Dict[str, str]] = {  # type: ignore
            normalize_locale(k): strings
            for k, v in internalizations.items()
            if (strings := v.get("strings"))
        }

        self.localizations: Dict[Locale, Dict[str, CommandLocalization]] = {  # type: ignore
            normalize_locale(k): commands
            for k, v in internalizations.items()
            if (commands := v.get("commands"))
        }

        self.context_menu_localizations: Dict[Locale, Dict[str, ContextMenuLocalization]] = {  # type: ignore
            normalize_locale(k): context_menus
            for k, v in internalizations.items()
            if (context_menus := v.get("context_menus"))
        }

        # Register hooks
        bot.before_invoke(self.set_current_locale)
        I18n.instance = self

    def localize(self, command: CommandT) -> CommandT:
        """A decorator to apply localizations to a command.

        Args:
            command: The command to localize

        Returns:
            The localized command
        """
        if isinstance(command, SlashCommand):
            self._localize_slash_command(command)
        elif isinstance(command, (MessageCommand, UserCommand)):
            self._localize_context_menu_command(command)

        return command

    def _localize_slash_command(self, command: SlashCommand) -> None:
        """Localize a slash command."""
        for locale, localized in self.localizations.items():
            if localizations := localized.get(command.qualified_name):
                self.command_localizer.localize(command, locale, localizations)

    def _localize_context_menu_command(self, command: MessageCommand | UserCommand) -> None:
        """Localize a context menu command."""
        for locale, localized in self.context_menu_localizations.items():
            if localizations := localized.get(command.qualified_name):
                self.context_menu_localizer.localize(command, locale, localizations)

    def localize_commands(self) -> None:
        """Localize all pending commands.

        This doesn't update commands on Discord and should be run prior to `bot.sync_commands`.
        """
        # Localize slash commands
        for locale, localized in self.localizations.items():
            for command_name, localizations in localized.items():
                command = utils.get(
                    self.bot._pending_application_commands, qualified_name=command_name
                )
                if command and isinstance(command, SlashCommand):
                    self.command_localizer.localize(command, locale, localizations)

        # Localize context menu commands
        for locale, localized in self.context_menu_localizations.items():
            for command_name, localizations in localized.items():
                command = utils.get(
                    self.bot._pending_application_commands, qualified_name=command_name
                )
                if command and isinstance(command, (MessageCommand, UserCommand)):
                    self.context_menu_localizer.localize(command, locale, localizations)

    async def set_current_locale(self, ctx: ApplicationContext) -> None:
        """Set the locale to be used in the next translation session.

        This is passed to `bot.before_invoke`.

        Args:
            ctx: The application context
        """
        if self.consider_user_locale:
            locale = ctx.locale or ctx.guild_locale
        else:
            locale = ctx.guild_locale

        if locale:
            self.current_locale = locale  # type: ignore

    @classmethod
    def get_text(cls, original: str, *format_args: object) -> str:
        """Translate a string based on the current locale.

        Args:
            original: The original string to translate
            *format_args: Optional format arguments for string formatting

        Returns:
            The translated string, or the original if no translation is found
        """
        self = I18n.instance

        # Get translation for current locale
        translations = self.translations.get(self.current_locale)
        text = translations.get(original) if translations else None

        # Fall back to original if no translation found
        if text is None:
            text = original

        # Apply formatting if args provided
        if format_args:
            return text.format(*format_args)

        return text


# Convenience function for translations
_ = I18n.get_text
