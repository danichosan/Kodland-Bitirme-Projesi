import unittest
from unittest.mock import AsyncMock, MagicMock
from commands.discord_command import register_commands
from discord.ext import commands

class TestDiscordBot(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        intents = commands.Intents.default()
        intents.message_content = True
        intents.members = True

        self.bot = commands.Bot(command_prefix='!', intents=intents)
        register_commands(self.bot)

    async def test_kayit_command(self):
        ctx = MagicMock()
        ctx.author.id = "123456"
        ctx.author.name = "testuser"
        ctx.send = AsyncMock()

        await self.bot.get_command('kayit').callback(ctx)

        ctx.send.assert_called_with(f'{ctx.author.mention}, kayıt işleminiz tamamlandı!')

    async def test_sec_command(self):
        ctx = MagicMock()
        ctx.author.id = "123456"
        ctx.author.mention = "@testuser"
        ctx.send = AsyncMock()

        await self.bot.get_command('sec').callback(ctx, career_choice="Yazılım Mühendisi")

        ctx.send.assert_called_with(f'{ctx.author.mention}, kariyer seçiminiz Yazılım Mühendisi olarak güncellendi!')

    async def test_yanit_command(self):
        ctx = MagicMock()
        ctx.author.id = "123456"
        ctx.author.mention = "@testuser"
        ctx.send = AsyncMock()

        await self.bot.get_command('yanit').callback(ctx, responses="Test responses")

        ctx.send.assert_called_with(f'{ctx.author.mention}, yanıtlarınız kaydedildi!')

if __name__ == '__main__':
    unittest.main()