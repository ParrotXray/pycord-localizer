"""Utility functions for pycord-localizer."""

from typing import Any, Literal, Union

from discord import MISSING, Option

from .types import Localizable, Locale

__all__ = (
    "add_localization",
    "normalize_locale",
)


def add_localization(
    target: Union[Localizable, Option, Any],
    field: Literal["name", "description"],
    locale: Locale,
    value: str,
) -> None:
    """Add a localization to a target object.

    Args:
        target: The object to add localization to (command, option, etc.)
        field: The field to localize ("name" or "description")
        locale: The target locale
        value: The localized value
    """
    attr = f"{field}_localizations"
    current = getattr(target, attr, None)

    if current in (None, MISSING):
        setattr(target, attr, {locale: value})
    else:
        current[locale] = value


def normalize_locale(locale: str) -> str:
    """Normalize locale string by replacing underscores with hyphens.

    Args:
        locale: The locale string to normalize (e.g., "zh_TW" or "zh-TW")

    Returns:
        Normalized locale string (e.g., "zh-TW")

    Examples:
        >>> normalize_locale("zh_TW")
        "zh-TW"
        >>> normalize_locale("en_US")
        "en-US"
    """
    return locale.replace("_", "-")
