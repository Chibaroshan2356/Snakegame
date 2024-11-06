import sqlite3
def create_database():
    connection = sqlite3.connect("snake_game.db")
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        password TEXT,
                        high_score INTEGER DEFAULT 0
                      )''')
    connection.commit()
    connection.close()
def register_user(username, password):
    try:
        connection = sqlite3.connect("snake_game.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        connection.commit()
    except sqlite3.IntegrityError:
        print("Username already exists.")
    finally:
        connection.close()
def validate_user(username, password):
    connection = sqlite3.connect("snake_game.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    connection.close()
    return user is not None
def get_high_score(username):
    connection = sqlite3.connect("snake_game.db")
    cursor = connection.cursor()
    cursor.execute("SELECT high_score FROM users WHERE username = ?", (username,))
    high_score = cursor.fetchone()
    connection.close()
    return high_score[0] if high_score else 0
def update_high_score(username, new_score):
    connection = sqlite3.connect("snake_game.db")
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET high_score = ? WHERE username = ? AND high_score < ?", (new_score, username, new_score))
    connection.commit()
    connection.close()
create_database()