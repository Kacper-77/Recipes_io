import streamlit as st
from db import get_recipes, save_recipe, delete_recipe, init_db
import time
from st_paywall import add_auth
import psycopg2
import pandas as pd
from datetime import datetime, timezone


@st.cache_resource
def get_connection():
    return psycopg2.connect(
        dbname=st.secrets["database"],
        user=st.secrets["username"],
        password=st.secrets["password"],
        host=st.secrets["host"],
        port=st.secrets["port"],
        sslmode=st.secrets["sslmode"]
    )


def insert_usage(email, output_tokens, input_tokens, input_text):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO usages (google_user_email, output_tokens, input_tokens, input_text) VALUES (%s, %s, %s, %s)
            """, (email, output_tokens, input_tokens, input_text))
            conn.commit()


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

init_db()

st.set_page_config(page_title="Recipes.io", layout="centered")
st.title(":orange[Twoje przepisy] 🍜")

with st.sidebar:
    st.write("Więcej informacji:")
    st.link_button("Polityka prywatnośći", "https://recipes-io-asstes.fra1.cdn.digitaloceanspaces.com/privacy_policy.pdf")
    st.link_button("Regulamin", "https://recipes-io-asstes.fra1.cdn.digitaloceanspaces.com/regulations.pdf")
    st.write("Kontakt: ks.kontaktowy7@gmail.com")
    st.write("Podoba ci się aplikacja? wesprzyj nas link poniżej:")
    st.link_button("🥰", "https://buymeacoffee.com/kacperszaruga", use_container_width=True)

    if st.session_state.get('email'):
        st.write(f"Zalogowano jako: {st.session_state['email']}")

try:
    add_auth(
        required=False,
        login_sidebar=False,
    )
except KeyError:
    pass
if st.session_state.get('email'):
    # Formularz dodawania nowego przepisu ręcznie
    recipe_name = st.text_input("Nazwa przepisu")
    recipe_content = st.text_area("Treść przepisu")

    if st.button("Dodaj przepis"):
        if recipe_name and recipe_content:
            save_recipe(recipe_name, recipe_content)
            message = st.toast("Zapisano! 🎊")

            time.sleep(2)

            message.empty()

        else:
            st.warning("Proszę wprowadzić nazwę i treść przepisu.")

    # Wyświetlanie zapisanych przepisów z bazy danych
    recipes = get_recipes()
    if recipes:
        for recipe in recipes:
            with st.expander(recipe[1]):  # recipe[1] to nazwa przepisu
                st.write(recipe[2])  # recipe[2] to treść przepisu
                if st.button("Usuń", key=f"delete_{recipe[0]}"):
                    delete_recipe(recipe[0])
                    st.toast("Usunięto 🗑️")
                    time.sleep(2)
                    st.rerun()
    else:
        st.write("Nie masz jeszcze żadnych przepisów.")
