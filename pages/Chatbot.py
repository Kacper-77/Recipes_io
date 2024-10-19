import streamlit as st
from langfuse.openai import OpenAI
from langfuse.decorators import observe
from dotenv import load_dotenv
from db import save_conversation

# Inicjalizacja konfiguracji strony
st.set_page_config(page_title="Chatbot", layout="centered")
st.title(":green[Chatbot] 🍽️")

# Wprowadzenie klucza API OpenAI
if "api_key" not in st.session_state:
    st.session_state.api_key = ""

api_key = st.text_input("Wprowadź swój klucz API OpenAI", type="password", value=st.session_state.api_key)

if api_key:
    st.session_state.api_key = api_key  # Zapisz klucz API w stanie sesji

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

        try:
            response = openai_client.chat.completions.create(
                model="gpt-4",
                messages=messages
            )
            return {
                "role": "assistant",
                "content": response.choices[0].message.content,
            }
        except Exception as e:
            return {
                "role": "assistant",
                "content": f"Coś poszło nie tak: {str(e)}"
            }

    # Inicjalizacja stanu sesji dla konwersacji
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    st.header(":orange[Aktualna konwersacja] 💬")

    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Sekcja do wpisania nowego promptu przez użytkownika
    prompt = st.chat_input("W czym mogę ci pomóc?")

    if prompt:
        # Dodanie wiadomości użytkownika do sesji
        user_message = {"role": "user", "content": prompt}
        with st.chat_message("user"):
            st.markdown(user_message["content"])

        st.session_state["messages"].append(user_message)

        # Uzyskanie odpowiedzi od chatbota
        chatbot_message = get_chatbot_reply(prompt, memory=st.session_state["messages"][-10:])

        # Wyświetlenie odpowiedzi chatbota
        with st.chat_message("assistant"):
            st.markdown(chatbot_message["content"])

        # Dodanie wiadomości chatbota do sesji
        st.session_state["messages"].append(chatbot_message)

        # Automatyczne zapisywanie konwersacji w bazie danych
        save_conversation(f"Konwersacja {len(st.session_state['messages']) // 2}", st.session_state["messages"])
else:
    st.warning("Proszę wprowadzić klucz API, aby korzystać z aplikacji.")
