import streamlit as st
from langfuse.openai import OpenAI
from langfuse.decorators import observe
from dotenv import load_dotenv
from db import save_conversation, save_recipe
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


with get_connection() as conn:
    with conn.cursor() as cur:
        cur.execute("""
CREATE TABLE IF NOT EXISTS usages (
    id SERIAL PRIMARY KEY,
    google_user_email VARCHAR(255),
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    output_tokens INTEGER,
    input_tokens INTEGER,
    input_text TEXT
)
        """)
        conn.commit()


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


# Inicjalizacja konfiguracji strony
st.set_page_config(page_title="Recipes.io", layout="centered")
st.title(":green[Chatbot] 🍽️")

with st.sidebar:
    st.write("Więcej informacji:")
    st.link_button("Polityka prywatnośći", "https://recipes-io-asstes.fra1.cdn.digitaloceanspaces.com/privacy_policy.pdf")
    st.link_button("Regulamin", "https://recipes-io-asstes.fra1.cdn.digitaloceanspaces.com/regulations.pdf")
    st.write("Kontakt: ks.kontaktowy7@gmail.com")
    st.write("Podoba ci się aplikacja? wesprzyj nas link poniżej:")
    st.link_button("🥰", "https://buymeacoffee.com/kacperszaruga", use_container_width=True)

    if st.session_state.get('email'):
        st.write(f"Zalogowano jako: {st.session_state['email']}")

        usage_df = get_current_month_usage_df(st.session_state['email'])
        st.write("W tym miesiącu użyłeś")
        c0, c1 = st.columns([1, 1])
        with c0:
            st.metric("Input tokenów", usage_df['input_tokens'].sum())
        with c1:
            st.metric("Output tokenów", usage_df['output_tokens'].sum())

try:
    add_auth(
        required=False,
        login_sidebar=False,
    )
except KeyError:
    pass

if st.session_state.get('email'):
    # Wprowadzenie klucza API OpenAI
    if "api_key" not in st.session_state:
        st.session_state.api_key = ""

    api_key = st.text_input("Wprowadź swój klucz API OpenAI", type="password", value=st.session_state.api_key)

    if api_key:
        st.session_state.api_key = api_key

        # Ładowanie zmiennych środowiskowych
        load_dotenv()

    # Inicjalizacja klienta OpenAI
        openai_client = OpenAI(api_key=st.session_state.api_key)

        @observe
        def get_chatbot_reply(user_prompt, memory):
            messages = [
                {
                    "role": "system",
                    "content": """
                        Jesteś ekspertem do spraw dietetyki,
                        przepisów i wszystkiego co z tym związane.
                        Wyliczaj makro dla każdego z dań i podawaj w przybliżeniu
                        kaloryczność. Odpowiadaj na pytania użytkownika w sposób zrozumiały.
                    """
                },
            ]
            for message in memory:
                messages.append({"role": message["role"], "content": message["content"]})

            messages.append({"role": "user", "content": user_prompt})
            
            # Wysyłanie zapytania do OpenAI
            response = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                stream=True,
            )
            
            usage = response["usage"]
            
            # Zapisanie użycia w bazie danych
            insert_usage(
                email=st.session_state['email'],
                output_tokens=usage['completion_tokens'],
                input_tokens=usage['prompt_tokens'],
                input_text=user_prompt,
            )
            
            return response
                  
        # Inicjalizacja stanu sesji dla konwersacji
        if "messages" not in st.session_state:
            st.session_state["messages"] = []

        if "chatbot_reply" not in st.session_state:
            st.session_state["chatbot_reply"] = ""

        # Przechowujemy stan widoczności sekcji zapisu
        if "show_save_section" not in st.session_state:
            st.session_state["show_save_section"] = False 

        st.header(":orange[Aktualna konwersacja] 💬")

        for message in st.session_state["messages"]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Sekcja do wpisania nowego promptu przez użytkownika
        prompt = st.chat_input("W czym mogę ci pomóc?")

        # Sekcja do obsługi promptu użytkownika
        if prompt:
            user_message = {"role": "user", "content": prompt}
            with st.chat_message("user"):
                st.markdown(user_message["content"])

            st.session_state["messages"].append(user_message)

            # Otrzymanie odpowiedzi chatbota i zapisanie zużycia
            chatbot_response = get_chatbot_reply(prompt, memory=st.session_state["messages"][-10:])
            
            with st.chat_message("assistant"):
                assistant_message = st.write_stream(chatbot_response)
                st.session_state["chatbot_reply"] = assistant_message

            st.session_state["messages"].append({"role": "assistant", "content": assistant_message})

            # Automatyczne zapisywanie konwersacji w bazie danych
            save_conversation(f"Konwersacja {len(st.session_state['messages']) // 2}", st.session_state["messages"])

        # Jeżeli chatbot odpowiedział, pokaż możliwość zapisania przepisu lub diety (ale nie porady)
        if st.session_state["chatbot_reply"]:
            if st.button("🍕"):
                st.session_state["show_save_section"] = not st.session_state["show_save_section"]

            if st.session_state["show_save_section"]:
                st.subheader("Zapisz przepis lub dietę")
                recipe_name = st.text_input("Podaj nazwę przepisu/diety", key="recipe_name_input")

                if st.button("Zapisz"):
                    if recipe_name:
                        save_recipe(recipe_name, st.session_state["chatbot_reply"])
                        info = st.toast("Zapisano! 🎊")
                        time.sleep(2)
                        info.empty()
                        st.session_state["chatbot_reply"] = ""
                    else:
                        st.warning("Proszę podać nazwę przepisu lub diety przed zapisaniem.")
    else:
        st.warning("Proszę wprowadzić klucz API, aby korzystać z aplikacji.")
