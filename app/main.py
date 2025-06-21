import streamlit as st
import pandas as pd                 # schon seit Week 2 nötig
import pathlib                      # Dateipfade (Week 2)
import sqlite3, random, json, datetime as dt   # NEW – Week 4

# Spielername in der Session ablegen, falls noch nicht vorhanden
if "player" not in st.session_state:
    st.session_state["player"] = ""


st.set_page_config(page_title="SpielStark – Hello Pitch", page_icon="⚽")

st.title("⚽ SpielStark – Hello Pitch!")
st.session_state["player"] = st.text_input(
    "Spielername eingeben", value=st.session_state["player"]
)

if st.session_state["player"]:
    st.success(f"Willkommen, {st.session_state['player']}! Bereit für dein bestes Training?")


    # ---------- WEEK 4 : Mood-Check-In ---------------------------------
    st.header("🧠 Tagesform")

    # Name kommt jetzt aus der Session
    player = st.session_state["player"]
    mood   = st.slider("Wie fühlst du dich heute?", 1, 10, 5, key="mood_slider")

    if st.button("Speichern"):
        if player:
            db = "app/data/spielstark.db"
            with sqlite3.connect(db) as con:
                con.execute(
                    "INSERT INTO mood_log(date, player, mood) VALUES (?,?,?)",
                    (dt.date.today().isoformat(), player, mood)
                )
            tips = json.load(open("app/data/mental_tips.json"))
            st.success(f"Gespeichert! 🤩  Tipp: {random.choice(tips)}")
        else:
            st.error("Bitte zuerst deinen Namen oben eingeben.")

    # Ø-Mood der letzten 7 Tage als Linie
    db = "app/data/spielstark.db"
    with sqlite3.connect(db) as con:
        df_mood = pd.read_sql_query(
            """
            SELECT date, AVG(mood) AS avg_mood
            FROM mood_log
            WHERE date >= date('now','-7 days')
            GROUP BY date
            ORDER BY date
            """,
            con,
            parse_dates=["date"],
        )

    if not df_mood.empty:
        st.line_chart(data=df_mood, x="date", y="avg_mood", height=200)
    # -------------------------------------------------------------------


# --- WEEK 2: Daten laden ---
data_file = pathlib.Path("app/data/sample_sessions.csv")

st.divider()               # hübscher Trenner

if data_file.exists():
    df = pd.read_csv(data_file, parse_dates=["date"])

    # --- NEW: Selectbox-Filter für Übung -----------------
    exercise_options = ["Alle"] + sorted(df.exercise.unique())
    choice = st.selectbox("Übung filtern", exercise_options)
    if choice != "Alle":
        df = df[df.exercise == choice]
    # -----------------------------------------------------

    st.subheader("📊 Letzte Trainingseinheiten")
    st.dataframe(df.tail(20))

    # Zwei Kennzahlen nebeneinander
    col1, col2 = st.columns(2)
    col1.metric("Ø Dauer (min)", f"{df.duration_min.mean():.1f}")
    col2.metric("Ø RPE", f"{df.rpe.mean():.1f}")

    st.bar_chart(df["exercise"].value_counts())
else:
    st.warning("Keine CSV gefunden – bitte erst Daten generieren.")
