import streamlit as st

st.set_page_config(page_title="SpielStark – Hello Pitch", page_icon="⚽")

st.title("⚽ SpielStark – Hello Pitch!")
spieler = st.text_input("Spielername eingeben")
if spieler:
    st.success(f"Willkommen, {spieler}! Bereit für dein bestes Training?")
