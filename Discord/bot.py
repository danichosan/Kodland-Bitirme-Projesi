import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import discord
from discord.ext import commands
from Discord import logic
from Discord.commands.discord_command import register_commands
import sqlite3
from discord import app_commands
from discord.ui import View, Button

print("Starting Discord bot...")

# Botun ayarları ve tokeni
TOKEN = 'TOKEN here'  # Discord token is now read from environment variable

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='/', intents=intents)
# When the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

    # Register commands
    register_commands(bot)

    # Initialize database tables
    logic.init_db()

    # Print users
    import sqlite3
    conn = sqlite3.connect('career_bot.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    print(cursor.fetchall())
    conn.close()

# Welcome message for new members
@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="general")
    if channel:
        await channel.send(
            f"Welcome, {member.mention}! I'm Drive My Career Bot.\n"
            "I can help you discover new and interesting career paths based on your expertise and degrees.\n"
            "For more info, type `/help`."
        )

# Error handling event
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Sorry, I could not find that command.')
    else:
        await ctx.send('An error occurred, please try again later.')
        raise error

class CareerView(View):
    def __init__(self, user_id, interests):
        super().__init__()
        self.user_id = user_id
        self.interests = interests
        # Add buttons for top 3 career suggestions
        self.suggestions = self.get_suggestions(interests)
        for suggestion in self.suggestions:
            self.add_item(Button(label=suggestion, style=discord.ButtonStyle.primary, custom_id=suggestion))

    def get_suggestions(self, interests):
        # Simple demo logic for suggestions
        interests_lower = interests.lower()
        options = [
            ("Software Developer", ["software", "coding", "developer", "engineer"]),
            ("Graphic Designer", ["design", "creative", "graphics"]),
            ("Digital Marketing Specialist", ["marketing", "social media", "advertising"]),
            ("Data Scientist", ["data", "analytics", "statistics"]),
            ("AI Engineer", ["ai", "machine learning", "artificial intelligence"]),
        ]
        matched = [name for name, keywords in options if any(k in interests_lower for k in keywords)]
        return matched if matched else ["Entrepreneur", "Project Manager", "System Administrator"]

    @discord.ui.button(label="More suggestions", style=discord.ButtonStyle.secondary)
    async def more_suggestions(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message(
            "Other career options: Game Developer, Web Developer, Mobile App Developer, Cyber Security Specialist.",
            ephemeral=True
        )

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        # Only allow the user who started the interaction
        return interaction.user.id == self.user_id

    async def on_button_click(self, interaction: discord.Interaction):
        chosen_career = interaction.data['custom_id']
        # Save chosen career to database
        conn = sqlite3.connect('career_bot.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET career_choice = ? WHERE discord_id = ?", (chosen_career, interaction.user.id))
        conn.commit()
        conn.close()
        await interaction.response.send_message(
            f"Your career choice '{chosen_career}' has been saved!", ephemeral=True
        )

@bot.tree.command(name="career", description="Get career suggestions based on your expertise or degrees")
async def career(interaction: discord.Interaction):
    await interaction.response.send_message(
        "Please describe your expertise, degrees, or areas you are skilled in (e.g. computer science, marketing, design):",
        ephemeral=True
    )

    def check(m):
        return m.author.id == interaction.user.id and m.channel == interaction.channel

    try:
        msg = await bot.wait_for('message', timeout=60.0, check=check)
        expertise = msg.content.strip()

        # Save expertise to database
        conn = sqlite3.connect('career_bot.db')
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO users (discord_id, interests) VALUES (?, ?)", (interaction.user.id, expertise))
        cursor.execute("UPDATE users SET interests = ? WHERE discord_id = ?", (expertise, interaction.user.id))
        conn.commit()
        conn.close()

        # Suggest careers based on expertise (simple demo logic)
        expertise_lower = expertise.lower()
        suggestions = []
        if "computer" in expertise_lower or "software" in expertise_lower or "engineering" in expertise_lower:
            suggestions.append("Software Developer")
            suggestions.append("AI Engineer")
            suggestions.append("Data Scientist")
        if "marketing" in expertise_lower or "business" in expertise_lower:
            suggestions.append("Digital Marketing Specialist")
            suggestions.append("Project Manager")
        if "design" in expertise_lower or "art" in expertise_lower:
            suggestions.append("Graphic Designer")
            suggestions.append("Web Developer")
        if not suggestions:
            suggestions = ["Entrepreneur", "System Administrator", "Game Developer"]

        view = View()
        for suggestion in suggestions[:3]:
            view.add_item(Button(label=suggestion, style=discord.ButtonStyle.primary, custom_id=suggestion))

        await interaction.followup.send(
            f"Based on your expertise, here are some career suggestions. Click a button to select:\nYour expertise: {expertise}",
            view=view,
            ephemeral=True
        )
    except Exception:
        await interaction.followup.send("No response received, please try again.", ephemeral=True)

# Run the bot
if __name__ == "__main__":
    if not TOKEN:
        print("ERROR: Discord bot token not set. Please set the DISCORD_BOT_TOKEN environment variable.")
    else:
        bot.run(TOKEN)