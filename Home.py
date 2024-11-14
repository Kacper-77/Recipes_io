import streamlit as st
from st_paywall import add_auth

# Ustawienia dla strony głównej
st.set_page_config(page_title="Recipes.io", layout="centered")

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
