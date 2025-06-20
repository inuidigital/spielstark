import streamlit as st

st.set_page_config(page_title="SpielStark – Hello Pitch", page_icon="⚽")

st.title("⚽ SpielStark – Hello Pitch!")
spieler = st.text_input("Spielername eingeben")
if spieler:
    st.success(f"Willkommen, {spieler}! Bereit für dein bestes Training?")

import pandas as pd, pathlib, streamlit as st   # Pd ist neu!

# --- WEEK 2: Daten laden ---
data_file = pathlib.Path("app/data/sample_sessions.csv")

st.divider()               # hübscher Trenner

if data_file.exists():
    df = pd.read_csv(data_file, parse_dates=["date"])

    st.subheader("📊 Letzte Trainingseinheiten")
    st.dataframe(df.tail(20))

    # Zwei Kennzahlen nebeneinander
    col1, col2 = st.columns(2)
    col1.metric("Ø Dauer (min)", f"{df.duration_min.mean():.1f}")
    col2.metric("Ø RPE", f"{df.rpe.mean():.1f}")

    st.bar_chart(df["exercise"].value_counts())
else:
    st.warning("Keine CSV gefunden – bitte erst Daten generieren.")
