import sqlite3

def init_db():
    conn = sqlite3.connect('career_bot.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            username TEXT,
            responses TEXT,
            career_choice TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_user(discord_id, username):
    conn = sqlite3.connect('career_bot.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (user_id, username, responses, career_choice)
        VALUES (?, ?, '', '')
        ON CONFLICT(user_id) DO UPDATE SET username=excluded.username
    ''', (discord_id, username))
    conn.commit()
    conn.close()

def save_user_responses(discord_id, responses):
    conn = sqlite3.connect('career_bot.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET responses = ? WHERE user_id = ?', (responses, discord_id))
    conn.commit()
    conn.close()

def update_career_choice(discord_id, career_choice):
    conn = sqlite3.connect('career_bot.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET career_choice = ? WHERE user_id = ?', (career_choice, discord_id))
    conn.commit()
    conn.close()

def add_career(career_name, description, skills_required, interest_area):
    conn = sqlite3.connect('career_bot.db')
    cursor = conn.cursor()

    cursor.execute('INSERT INTO careers (career_name, description, skills_required, interest_area) VALUES (?, ?, ?, ?)',
                   (career_name, description, skills_required, interest_area))

    conn.commit()
    conn.close()

def get_career_by_interest(interest_area):
    conn = sqlite3.connect('career_bot.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM careers WHERE interest_area = ?', (interest_area,))
    careers = cursor.fetchall()

    conn.close()
    return careers

def get_user(user_id):
    conn = sqlite3.connect('career_bot.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()

    conn.close()
    return user

def get_career_options():
    return [
        ("Yazılım Geliştirici",),
        ("Veri Bilimci",),
        ("Tasarımcı",),
        ("Siber Güvenlik Uzmanı",),
        ("Oyun Geliştirici",),
        ("Web Geliştirici",),
        ("Mobil Uygulama Geliştirici",),
        ("Proje Yöneticisi",),
        ("Sistem Yöneticisi",),
        ("Yapay Zeka Mühendisi",)
    ]
