import sqlite3
def create_connection():
    conn = sqlite3.connect('snake_game.db')
    return conn
def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL)''')
    conn.commit()
    conn.close()
def register_user(username, password):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()
def validate_user(username, password):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    stored_password = cursor.fetchone()
    conn.close()
    if stored_password:
        return stored_password[0] == password
    return False
def attempt_login(username, password):
    return validate_user(username, password)
def attempt_register(username, password):
    return register_user(username, password)
def get_high_score():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT score FROM highscores ORDER BY score DESC LIMIT 1")
    score = cursor.fetchone()
    conn.close()
    return score[0] if score else 0
def save_high_score(username, score):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO highscores (username, score) VALUES (?, ?)", (username, score))
    conn.commit()
    conn.close()
create_table()