from threading import Thread
from WebSite.main import app
from Discord.bot import bot

def run_web():
    app.run(host='0.0.0.0', port=5000)

def run_discord():
    bot.run('TOKEN here')

if __name__ == '__main__':
    Thread(target=run_web).start()
    run_discord()