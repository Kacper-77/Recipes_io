import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime, timezone
import pandas as pd
import streamlit as st


# Funkcja do nawiązywania połączenia z bazą danych PostgreSQL
def get_connection():
    return psycopg2.connect(
        dbname=st.secrets["database"],
        user=st.secrets["username"],
        password=st.secrets["password"],
        host=st.secrets["host"],
        port=st.secrets["port"],
        sslmode=st.secrets["sslmode"]
    )


# Funkcja do inicjalizacji tabel w bazie danych PostgreSQL
def init_db():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    messages TEXT NOT NULL
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS recipes (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    content TEXT NOT NULL,
                    user_email TEXT NOT NULL
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS usages (
                    id SERIAL PRIMARY KEY,
                    google_user_email TEXT NOT NULL,
                    output_tokens INTEGER NOT NULL,
                    input_tokens INTEGER NOT NULL,
                    input_text TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT NOW()
                );
            """)
            conn.commit()


# Funkcja do zapisywania konwersacji w bazie danych
def save_conversation(name, messages):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO conversations (name, messages) 
                VALUES (%s, %s);
            """, (name, str(messages)))
            conn.commit()


# Funkcja do zapisywania przepisu w bazie danych
def save_recipe(name, content, user_email):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO recipes (name, content, user_email) 
                VALUES (%s, %s, %s);
            """, (name, content, user_email))
            conn.commit()


# Funkcja do pobierania przepisów dla zalogowanego użytkownika
def get_recipes(user_email):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT * FROM recipes WHERE user_email = %s;
            """, (user_email,))
            recipes = cur.fetchall()
    return recipes


# Funkcja do usuwania przepisu z bazy danych
def delete_recipe(recipe_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                DELETE FROM recipes WHERE id = %s;
            """, (recipe_id,))
            conn.commit()


# Funkcja do dodawania zużycia
def insert_usage(email, output_tokens, input_tokens, input_text):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO usages (google_user_email, output_tokens, input_tokens, input_text) 
                VALUES (%s, %s, %s, %s);
            """, (email, output_tokens, input_tokens, input_text))
            conn.commit()


# Funkcja do wydobywania zużycia z bieżącego miesiąca
def get_current_month_usage_df(email):
    with get_connection() as conn:
        now = datetime.now(timezone.utc)
        start_date = datetime(now.year, now.month, 1)
        with conn.cursor() as cur:
            cur.execute("""
                SELECT * FROM usages 
                WHERE google_user_email = %s AND created_at >= %s;
            """, (email, start_date))
            rows = cur.fetchall()
            columns = [desc[0] for desc in cur.description]
            df_usage = pd.DataFrame(rows, columns=columns)
    return df_usage
