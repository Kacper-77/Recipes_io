import streamlit as st
from db import get_recipes, save_recipe, delete_recipe, init_db
import time
from st_paywall import add_auth

init_db()

st.title(":orange[Twoje przepisy] 🍜")

with st.sidebar:
    if st.session_state.get('email'):
        st.write(f"Zalogowano jako: {st.session_state['email']}")

    st.write("Więcej informacji:")
    col1, col2 = st.columns(2)
    with col1:
        st.link_button("Polityka prywatności", "https://recipes-io-asstes.fra1.cdn.digitaloceanspaces.com/privacy_policy.pdf")
    with col2:
        st.link_button("Regulamin", "https://recipes-io-asstes.fra1.cdn.digitaloceanspaces.com/regulations.pdf")
    st.write("Kontakt: ks.kontaktowy7@gmail.com")
    st.write("Podoba ci się aplikacja? wesprzyj nas link poniżej:")
    st.link_button("🥰", "https://buymeacoffee.com/kacperszaruga", use_container_width=True)

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
    user_email = st.session_state.get('email')
    if st.button("Dodaj przepis"):
        if recipe_name and recipe_content:
            save_recipe(recipe_name, recipe_content, user_email)
            message = st.toast("Zapisano! 🎊")

            time.sleep(2)

            message.empty()

        else:
            st.warning("Proszę wprowadzić nazwę i treść przepisu.")

    # Wyświetlanie zapisanych przepisów z bazy danych
    user_email = st.session_state.get('email')
    if user_email:
        recipes = get_recipes(user_email)
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