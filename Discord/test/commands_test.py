import unittest
from commands.discord_command import register_commands
from discord.ext import commands

class TestCommandRegistration(unittest.TestCase):
    def setUp(self):
        intents = commands.Intents.default()
        intents.message_content = True
        self.bot = commands.Bot(command_prefix='!', intents=intents)
        register_commands(self.bot)

    def test_commands_registered(self):
        command_names = [command.name for command in self.bot.commands]
        self.assertIn('kayit', command_names)
        self.assertIn('sec', command_names)
        self.assertIn('kariyer', command_names)
        self.assertIn('yanit', command_names)

if __name__ == '__main__':
    unittest.main()