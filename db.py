import sqlite3
import psycopg2
from datetime import datetime, timezone
import pandas as pd
import streamlit as st


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


# Funkcja do nawiązywania połączenia
def get_connection():
    return psycopg2.connect(
        dbname=st.secrets["database"],
        user=st.secrets["username"],
        password=st.secrets["password"],
        host=st.secrets["host"],
        port=st.secrets["port"],
        sslmode=st.secrets["sslmode"]
    )


# Funkcja do dodawania zużycia
def insert_usage(email, output_tokens, input_tokens, input_text):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO usages (google_user_email, output_tokens, input_tokens, input_text) VALUES (%s, %s, %s, %s)
            """, (email, output_tokens, input_tokens, input_text))
            conn.commit()


# Funkcja do wydobywania zużycia
def get_current_month_usage_df(email):
    with get_connection() as conn:
        now = datetime.now(timezone.utc)
        start_date = datetime(now.year, now.month, 1)
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM usages WHERE google_user_email = %s AND created_at >= %s", (email, start_date))
            rows = cur.fetchall()
            columns = [desc[0] for desc in cur.description]
            df_usage = pd.DataFrame(rows, columns=columns)

    return df_usage