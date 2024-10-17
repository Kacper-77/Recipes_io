import streamlit as st
from langfuse.openai import OpenAI
from langfuse.decorators import observe
from dotenv import load_dotenv
from db import init_db, save_conversation, save_recipe, get_recipes, delete_recipe

# Inicjalizacja bazy danych
init_db()
st.set_page_config(page_title="Recipes.io", layout="centered")
st.title("Recipes.:green[i]:orange[o] 👨🏻‍🍳")

# Wprowadzenie klucza API
api_key = st.text_input("Wprowadź swój klucz API OpenAI:", type="password")

if not api_key:
    st.warning("Proszę wprowadzić klucz API, aby korzystać z aplikacji.")
    st.stop()

load_dotenv()

openai_client = OpenAI(api_key=api_key)


@observe
def get_chatbot_reply(user_prompt, memory):
    messages = [
        {
            "role": "system",
            "content": """
                Jesteś ekspertem do spraw dietetyki,
                przepisów i wszystkiego co z tym związane,
                do tego wyliczaj makro dla każdego z dań i podawaj w przybliżeniu
                kaloryczność. Odpowiadaj na pytania użytkownika w sposób zrozumiały
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


if "conversations" not in st.session_state:
    st.session_state["conversations"] = []

if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Tworzenie tabów
tabs = st.tabs(["Chatbot", "Twoje przepisy"])

# Tab Chatbot
with tabs[0]:
    st.header("Chat")

    # Wyświetlenie wszystkich wiadomości
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Wprowadzenie nowego promptu na dole
    prompt = st.chat_input("W czym mogę ci pomóc?")

    if prompt:
        user_message = {"role": "user", "content": prompt}
        with st.chat_message("user"):
            st.markdown(user_message["content"])

        st.session_state["messages"].append(user_message)

        chatbot_message = get_chatbot_reply(prompt, memory=st.session_state["messages"][-10:])

        with st.chat_message("assistant"):
            st.markdown(chatbot_message["content"])

        st.session_state["messages"].append(chatbot_message)
        # Automatyczne zapisywanie konwersacji
        save_conversation(f"Konwersacja {len(st.session_state['conversations']) + 1}", st.session_state["messages"])

# Tab Przepisy
with tabs[1]:
    st.header("Dodaj przepis 🍜")

    recipe_name = st.text_input("Nazwa przepisu")
    recipe_content = st.text_area("Treść przepisu")

    if st.button("Dodaj przepis"):
        if recipe_name and recipe_content:
            save_recipe(recipe_name, recipe_content)
            st.success("Przepis został dodany!")
        else:
            st.warning("Proszę wprowadzić nazwę i treść przepisu.")

    # Wyświetlenie przepisów
    st.header(":orange[Twoje przepisy]")
    recipes = get_recipes()
    if recipes:
        for recipe in recipes:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.subheader(recipe[1])  # Nazwa przepisu
                st.write(recipe[2])      # Treść przepisu
            with col2:
                if st.button("Usuń", key=f"delete_{recipe[0]}"):
                    delete_recipe(recipe[0])  # Usuń przepis z bazy danych
                    st.success("Przepis został usunięty!")
                    st.experimental_rerun()  # Odświeżenie strony po usunięciu
    else:
        st.write("Nie masz jeszcze żadnych przepisów")
