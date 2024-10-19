import streamlit as st
from db import get_recipes, save_recipe, delete_recipe, init_db
import time

init_db()

st.title(":orange[Twoje przepisy] 🍜")

recipe_name = st.text_input("Nazwa przepisu")
recipe_content = st.text_area("Treść przepisu")

if st.button("Dodaj przepis"):
    if recipe_name and recipe_content:
        save_recipe(recipe_name, recipe_content)
        message = st.success("Przepis został dodany!")

        time.sleep(3)

        message.empty()

    else:
        st.warning("Proszę wprowadzić nazwę i treść przepisu.")

recipes = get_recipes()
if recipes:
    for recipe in recipes:
        with st.expander(recipe[1]):
            st.write(recipe[2])
            if st.button("Usuń", key=f"delete_{recipe[0]}"):
                delete_recipe(recipe[0])
                st.rerun()
else:
    st.write("Nie masz jeszcze żadnych przepisów.")
