import sqlite3


# Funkcja do połączenia z bazą danych SQLite
def init_db():
    conn = sqlite3.connect("conversations.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS conversations
                 (id INTEGER PRIMARY KEY, name TEXT, messages TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS recipes
                 (id INTEGER PRIMARY KEY, name TEXT, content TEXT)''')
    conn.commit()
    conn.close()


# Funkcja do zapisywania konwersacji w bazie danych
def save_conversation(name, messages):
    conn = sqlite3.connect("conversations.db")
    c = conn.cursor()
    c.execute("INSERT INTO conversations (name, messages) VALUES (?, ?)", (name, str(messages)))
    conn.commit()
    conn.close()


# Funkcja do zapisywania przepisu w bazie danych
def save_recipe(name, content):
    conn = sqlite3.connect("conversations.db")
    c = conn.cursor()
    c.execute("INSERT INTO recipes (name, content) VALUES (?, ?)", (name, content))
    conn.commit()
    conn.close()


# Funkcja do pobierania przepisów z bazy danych
def get_recipes():
    conn = sqlite3.connect("conversations.db")
    c = conn.cursor()
    c.execute("SELECT * FROM recipes")
    recipes = c.fetchall()
    conn.close()
    return recipes


# Funkcja do usuwania przepisu z bazy danych
def delete_recipe(recipe_id):
    conn = sqlite3.connect("conversations.db")
    c = conn.cursor()
    c.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
    conn.commit()
    conn.close()
