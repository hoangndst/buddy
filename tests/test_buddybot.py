import unittest

import discord
from discord.ext import commands

from main import BuddyBot


class BuddyBotConfigurationTests(unittest.IsolatedAsyncioTestCase):
    async def test_initial_extensions_are_preserved(self):
        intents = discord.Intents.none()
        bot = BuddyBot(
            commands.when_mentioned_or("$"),
            initial_extensions=["cogs.fake"],
            intents=intents,
        )
        try:
            self.assertEqual(bot.initial_extensions, ["cogs.fake"])
            self.assertIsNone(bot.testing_guild_id)
        finally:
            await bot.close()

    async def test_testing_guild_id_is_stored(self):
        intents = discord.Intents.none()
        bot = BuddyBot(
            commands.when_mentioned_or("$"),
            initial_extensions=[],
            intents=intents,
            testing_guild_id=987654321,
        )
        try:
            self.assertEqual(bot.testing_guild_id, 987654321)
        finally:
            await bot.close()
