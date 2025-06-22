import streamlit as st
import pandas as pd          # schon seit Week 2 nötig
import pathlib               # Dateipfade
import sqlite3, random, json, datetime as dt
import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent))
from app.ai_utils import get_analysis, get_plan

# ------------------------------------------------------------
# Mapping Buchstabe ➜ Klartext (wird im UI angezeigt)
# ------------------------------------------------------------
POS_TXT = {
    "A": "Torwart",
    "B": "Rechtsverteidiger",
    "C": "Innenverteidiger",
    "D": "Linksverteidiger",
    "E": "6er (Def. MF)",
    "F": "8er (Zentr. MF)",
    "G": "10er (Off. MF)",
    "H": "Rechter Flügel",
    "I": "Linker Flügel",
    "J": "Mittelstürmer",
    "K": "Hängende Spitze",
}

SKILL_TXT = {
    "A": "Technik / Ballbehandlung",
    "B": "Schnelligkeit / Antritt",
    "C": "Spielintelligenz / Überblick",
    "D": "Physis / Kraft & Ausdauer",
    "E": "Mentalität / Fokus",
}

FREQ_TXT = {
    "A": "Gar nicht",
    "B": "1× pro Woche",
    "C": "2–3× pro Woche",
    "D": "4–5× pro Woche",
    "E": "Täglich / fast täglich",
}

DEC_TXT = {
    "A": "Sicherheitspass zurück / quer",
    "B": "1-gegen-1-Dribbling",
    "C": "Sofort schneller Steilpass",
    "D": "Ball behaupten, warten",
    "E": "Direkt aufs Tor abschließen",
}

GOAL_TXT = {
    "A": "Spaß-Kicker Freizeitliga",
    "B": "Stammspieler Verein",
    "C": "Leistungsträger Region/Bezirk",
    "D": "NLZ-Spieler (hoher Aufwand)",
    "E": "U-Nationalteam / Profiweg",
}
# ------------------------------------------------------------


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

# ---------- Onboarding-Fragebogen ----------------------------------
if "profile" not in st.session_state:
    st.session_state["profile"] = {}

with st.form("onboard"):
    st.subheader("🏁 Dein Spielerprofil")

    # 1 Lieblingsposition
    pos = st.radio(
        "Lieblingsposition?",
        options=list(POS_TXT),                    # gibt A-K zurück
        format_func=lambda k: POS_TXT[k]          # zeigt Klartext
    )

    # 2 Talent / Schwäche – nebeneinander
    col1, col2 = st.columns(2)
    with col1:
        talent = st.selectbox(
            "Größtes Talent",
            options=list(SKILL_TXT),
            format_func=lambda k: SKILL_TXT[k]
        )
    with col2:
        weakness = st.selectbox(
            "Größte Schwäche",
            options=list(SKILL_TXT),
            format_func=lambda k: SKILL_TXT[k]
        )

    # 3 Trainingshäufigkeit
    freq = st.radio(
        "Extra-Training / Woche?",
        options=list(FREQ_TXT),
        format_func=lambda k: FREQ_TXT[k]
    )

    # 4 Entscheidung unter Druck
    decision = st.radio(
        "Entscheidung unter Druck",
        options=list(DEC_TXT),
        format_func=lambda k: DEC_TXT[k]
    )

    # 5 Ziel & Einsatzbereitschaft
    goal = st.radio(
        "Ziel in 3 Jahren?",
        options=list(GOAL_TXT),
        format_func=lambda k: GOAL_TXT[k]
    )

    submitted = st.form_submit_button("Analyse erstellen")

if submitted:
    profile = {
        "Q1": pos,
        "Q2_Talent": talent,
        "Q2_Schwäche": weakness,
        "Q3": freq,
        "Q4": decision,
        "Q5": goal,
        "name": st.session_state["player"],
    }
    st.session_state["profile"]  = profile
    analysis = get_analysis(profile)
    st.session_state["analysis"] = analysis
    st.markdown("## Deine Analyse")
    st.markdown(analysis, unsafe_allow_html=True)
# -------------------------------------------------------------------

# ---------- Paywall & 6-Wochen-Plan --------------------------------
if st.session_state.get("analysis") and not st.session_state.get("paid"):
    st.info("🎁 Analyse gratis ✔️  \n🔒 Pers. 6-Wochen-Plan: 4,99 €/Monat")
    if st.button("Abo abschließen (Demo)"):
        st.session_state["paid"] = True
    st.stop()

if st.session_state.get("paid"):
    if "plan" not in st.session_state:
        st.session_state["plan"] = get_plan(st.session_state["analysis"])
        (pathlib.Path("app/data") /
         f"plan_{st.session_state['player']}.md").write_text(
             st.session_state["plan"], encoding="utf-8")
    st.markdown("## Dein 6-Wochen-Trainingsplan")
    st.markdown(st.session_state["plan"], unsafe_allow_html=True)
# -------------------------------------------------------------------


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
