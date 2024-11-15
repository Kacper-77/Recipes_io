import streamlit as st
from st_paywall import add_auth
import psycopg2
import pandas as pd
from datetime import datetime, timezone


# Ustawienia dla strony głównej
st.set_page_config(page_title="Recipes.io", layout="centered")

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

# Strona główna
st.title("Witamy w Recipes.:green[i]:orange[o] 👨🏻‍🍳")
st.subheader(":red[Dziękujemy, że postanowiłeś/aś nam zaufać!]")

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

st.write("""
**Krótko** o **nas**:
       
 Nasza aplikacja jest od ludzi dla ludzi, chcemy aby każdy mógł z niej korzystać
  z tego tytułu postaraliśmy się aby wszystko było jak najbardziej intucyjne.
       
 Dlaczego akurat taka aplikacja? Odpowiedź jest prosta autor tej aplikacji sam cierpi na refluks
  i postanowił on stworzyć coś co będzie w stanie pomóc ludziom z podobnymi dolegliwościami i nie tylko,
  poza tym autor aplikacji jest zwolennikiem zdrowego trybu życia i jest to
  w pewien sposób manifest który ma na celu przekonać ludzi do dbania o siebię.
         
Ale nie tylko chorzy mogą z niej korzystać, bo może dosłownie każdy,
  zaczynając od pełnej diety idąc poprzez porady żywieniowe kończąc na braku pomysłu na obiad.
**Instrukcja korzystania z aplikacji**:
- Zaloguj się przez swoje konto Google
- Aplikacja jest podzielona na dwie głowne sekcję chatbot oraz przepisy
- Strona :green[**chatbot**] to nasz specjalista który pomoże ci z każdym problemem.
- Strona :orange[**przepisy**] to strona w której można zapisać sobie każdy dowolny przepis lub dietę
  np. wygenerowany przez naszego :green[**specljalistę**]. Wystarczy kliknąć 🍕 pod wiadomością od chatbota.
        
To tyle życzymy :red[**SMACZNEGO**]!
""")

try:
    add_auth(
        required=False,
        login_sidebar=False,
    )
except KeyError:
    pass
