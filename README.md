# pycord-localizer

[![PyPI version](https://badge.fury.io/py/pycord-localizer.svg)](https://badge.fury.io/py/pycord-localizer)
[![Python versions](https://img.shields.io/pypi/pyversions/pycord-localizer.svg)](https://pypi.org/project/pycord-localizer/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Comprehensive internationalization (i18n) library for Pycord**

## Installation

```bash
# linux / macOS
python3 -m pip install pycord-i18n

# windows
python -m pip install pycord-i18n
```

## Quick Start

### 1. Create Localization Files

Create JSON files for each language you want to support:

**zh-TW.json**
```json
{
    "strings": {
        "Hello, world!": "你好，世界！"
    },
    "commands": {
        "greet": {
            "name": "問候",
            "description": "向使用者問候",
            "options": {
                "user": {
                    "name": "使用者",
                    "description": "選擇要問候的使用者"
                }
            }
        }
    },
    "context_menus": {
        "user_info": {
            "name": "使用者資訊"
        }
    }
}
```

### 2. Setup in Your Bot

```python
import json
from discord import Bot, Option
from pycord_localizer import I18n, _

# Load localization files
with open("zh-TW.json", encoding="utf-8") as f:
    zh_tw = json.load(f)

with open("ja.json", encoding="utf-8") as f:
    ja = json.load(f)

# Create bot and setup i18n
bot = Bot()
i18n = I18n(bot, zh_TW=zh_tw, ja=ja)

# Define commands
@i18n.localize
@bot.slash_command()
async def greet(ctx, user: Option(discord.Member, "Select a user")):
    await ctx.respond(_("Hello, {0}!", user.mention))

bot.run("YOUR_TOKEN")
```

## Documentation

### Supported Locales

```python
"id", "da", "de", "en-GB", "en-US", "es-ES", "es-419", "fr", "hr", "it", 
"lt", "hu", "nl", "no", "pl", "pt-BR", "ro", "fi", "sv-SE", "vi", "tr", 
"cs", "el", "bg", "ru", "uk", "hi", "th", "zh-CN", "ja", "zh-TW", "ko"
```

### Localization Structure

```json
{
    "strings": {
        "key": "translated text",
        "format {0}": "格式化 {0}"
    },
    "commands": {
        "command_name": {
            "name": "localized_name",
            "description": "localized_description",
            "options": {
                "option_name": {
                    "name": "localized_option",
                    "description": "localized_description",
                    "choices": {
                        "choice_value": "localized_choice_name"
                    }
                }
            }
        }
    },
    "context_menus": {
        "context_menu_name": {
            "name": "localized_menu_name"
        }
    }
}
```

## Examples

### Slash Command with Choices

```python
from discord import Option, OptionChoice

@i18n.localize
@bot.slash_command()
async def language(
    ctx,
    lang: Option(
        str,
        "Choose your preferred language",
        choices=[
            OptionChoice(name="English", value="en-US"),
            OptionChoice(name="Traditional Chinese", value="zh-TW"),
            OptionChoice(name="Japanese", value="ja"),
            OptionChoice(name="German", value="de"),
        ]
    )
):
    await ctx.respond(f"Language set to: {lang}")
```

**Localization file:**
```json
{
    "commands": {
        "language": {
            "name": "語言",
            "description": "選擇你的偏好語言",
            "options": {
                "lang": {
                    "name": "語言",
                    "description": "選擇你偏好的語言",
                    "choices": {
                        "en-US": "英文",
                        "zh-TW": "繁體中文",
                        "ja": "日文",
                        "de": "德文"
                    }
                }
            }
        }
    }
}
```

### Context Menu Commands

```python
# User command (right-click on user)
@i18n.localize
@bot.user_command(name="user_info")
async def user_info(ctx, member):
    await ctx.respond(_("User: {0}", member.name))

# Message command (right-click on message)
@i18n.localize
@bot.message_command(name="get_id")
async def get_id(ctx, message):
    await ctx.respond(_("Message ID: {0}", message.id))
```

### Batch Localization

Instead of decorating each command, you can localize all at once:

```python
# Define all commands first
@bot.slash_command()
async def hello(ctx):
    await ctx.respond(_("Hello!"))

@bot.user_command(name="user_info")
async def user_info(ctx, member):
    await ctx.respond(f"User: {member.name}")

# Then localize all commands
i18n.localize_commands()
```

### String Formatting

```python
# Simple formatting
await ctx.respond(_("Hello, {0}!", user.name))

# Multiple arguments
await ctx.respond(_("User {0} has {1} points", name, points))
```

### User vs Server Locale

```python
# Default: Use server locale
i18n = I18n(bot, zh_TW=zh_tw)

# Use user's preferred locale
i18n = I18n(bot, consider_user_locale=True, zh_TW=zh_tw)
```