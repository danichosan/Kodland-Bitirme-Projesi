import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import discord
from discord.ext import commands
from Discord import logic
from Discord.commands.discord_command import register_commands
import sqlite3

print("Discord botu başlatılıyor...")

# Botun ayarları ve tokeni
TOKEN = os.getenv('DISCORD_BOT_TOKEN')  # Discord token is now read from environment variable

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Bot başlatıldığında çalışacak event
@bot.event
async def on_ready():
    print(f'{bot.user} olarak giriş yapıldı!')

    # Komutları kaydetme
    register_commands(bot)

    # Veritabanı tablolarını başlatma
    logic.init_db()

    # Kullanıcıları yazdır
    import sqlite3
    conn = sqlite3.connect('career_bot.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    print(cursor.fetchall())
    conn.close()

# Yeni üye katıldığında hoşgeldin mesajı gönderme
@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="genel")
    if channel:
        await channel.send(f"Hoşgeldin, {member.mention}! Drive My Career sunucusuna katıldığın için teşekkür ederiz.")

# Hata yönetimi için event
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Üzgünüm, böyle bir komut bulamadım.')
    else:
        await ctx.send('Bir hata oluştu, lütfen daha sonra tekrar dene.')
        raise error

# Botu çalıştır
if __name__ == "__main__":
    if not TOKEN:
        print("ERROR: Discord bot token not set. Please set the DISCORD_BOT_TOKEN environment variable.")
    else:
        bot.run(TOKEN)

os.chdir('c:\\Users\\Administrator\\Desktop\\dani\\cd\\DMC\\Discord')