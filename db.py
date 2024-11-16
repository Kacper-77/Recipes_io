import psycopg2
from psycopg2 import sql

# Function to connect to the PostgreSQL database
def init_db():
    conn = psycopg2.connect(
        dbname="your_dbname",
        user="your_username",
        password="your_password",
        host="your_host",
        port="your_port"
    )
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS conversations
                 (id SERIAL PRIMARY KEY, name TEXT, messages TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS recipes
                 (id SERIAL PRIMARY KEY, name TEXT, content TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id SERIAL PRIMARY KEY, email TEXT UNIQUE, password TEXT)''')
    conn.commit()
    conn.close()

# Function to save a conversation in the database
def save_conversation(name, messages):
    conn = psycopg2.connect(
        dbname="your_dbname",
        user="your_username",
        password="your_password",
        host="your_host",
        port="your_port"
    )
    c = conn.cursor()
    c.execute("INSERT INTO conversations (name, messages) VALUES (%s, %s)", (name, str(messages)))
    conn.commit()
    conn.close()

# Function to save a recipe in the database
def save_recipe(name, content):
    conn = psycopg2.connect(
        dbname="your_dbname",
        user="your_username",
        password="your_password",
        host="your_host",
        port="your_port"
    )
    c = conn.cursor()
    c.execute("INSERT INTO recipes (name, content) VALUES (%s, %s)", (name, content))
    conn.commit()
    conn.close()

# Function to get recipes from the database
def get_recipes():
    conn = psycopg2.connect(
        dbname="your_dbname",
        user="your_username",
        password="your_password",
        host="your_host",
        port="your_port"
    )
    c = conn.cursor()
    c.execute("SELECT * FROM recipes")
    recipes = c.fetchall()
    conn.close()
    return recipes

# Function to delete a recipe from the database
def delete_recipe(recipe_id):
    conn = psycopg2.connect(
        dbname="your_dbname",
        user="your_username",
        password="your_password",
        host="your_host",
        port="your_port"
    )
    c = conn.cursor()
    c.execute("DELETE FROM recipes WHERE id = %s", (recipe_id,))
    conn.commit()
    conn.close()

# Function to register a user
def register_user(email, password):
    conn = psycopg2.connect(
        dbname="your_dbname",
        user="your_username",
        password="your_password",
        host="your_host",
        port="your_port"
    )
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, password))
        conn.commit()
    except psycopg2.IntegrityError:
        return False
    finally:
        conn.close()
    return True

# Function to authenticate a user
def authenticate_user(email, password):
    conn = psycopg2.connect(
        dbname="your_dbname",
        user="your_username",
        password="your_password",
        host="your_host",
        port="your_port"
    )
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
    user = c.fetchone()
    conn.close()
    return user is not None
