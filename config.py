import streamlit as st


def get_config():
    config = st.secrets["redirect_uri"].startswith("https://recipes-io.streamlit.app")
    
    config["redirect_uri"] = config["redirect_uri"].rstrip('/')
   
    return config
