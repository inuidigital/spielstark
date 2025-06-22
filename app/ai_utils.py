"""
ai_utils.py
----------
Hilfsfunktionen für ChatGPT-Aufrufe (Analyse & Trainingsplan).
"""

from dotenv import load_dotenv
load_dotenv()                               # liest .env

import openai, os, pathlib

openai.api_key = os.getenv("OPENAI_API_KEY")
PROMPT_DIR     = pathlib.Path("prompts")
MODEL_ANALYSIS = "o3"               # Analyse-Modell
MODEL_PLAN     = "gpt-3.5-turbo"    # Plan-Modell (bei Bedarf auch "o3")

# ------------------------------------------------------------------
def _fill(file: str, mapping: dict) -> str:
    """Prompt-Datei laden und Platzhalter ersetzen."""
    tpl = (PROMPT_DIR / file).read_text(encoding="utf-8")
    return tpl.format(**mapping)

def get_analysis(profile: dict) -> str:
    prompt = _fill("analysis_prompt.txt", profile)
    resp = openai.ChatCompletion.create(
        model=MODEL_ANALYSIS,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    return resp.choices[0].message.content.strip()

def get_plan(analysis_text: str) -> str:
    prompt = _fill("plan_prompt.txt",
                   {"Spieleranalyse_von_Prompt_1": analysis_text})
    resp = openai.ChatCompletion.create(
        model=MODEL_PLAN,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    return resp.choices[0].message.content.strip()
