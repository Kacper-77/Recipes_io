import streamlit as st

# Ustawienia dla strony głównej
st.set_page_config(page_title="Recipes.io", layout="centered")

# Strona główna
st.title("Witamy w Recipes.:green[i]:orange[o] 👨🏻‍🍳")
st.subheader(":red[Dziękujemy, że postanowiłeś/aś nam zaufać!]")
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
- Aplikacja jest podzielona na dwie głowne sekcję chatbot oraz przepisy
- Aby móc korzystać z chatbota czyli naszego specjalisty do spraw żywieniowych
  wystarczy **podać klucz API**
- Strona :orange[**przepisy**] to strona w której można zapisać sobie każdy dowolny przepis
  np. wygenerowany przez naszego :green[**specljalistę**]
        
To tyle życzymy :red[**SMACZNEGO**]!
""")

st.write("""
Masz pomysł na usprawnienie naszej aplikacji? Może ci czegoś brakuję?
         
**Napisz do nas**: example.email@recipes.io
"""
)
