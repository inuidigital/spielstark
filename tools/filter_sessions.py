"""
filter_sessions.py
------------------
Kleines Kommandozeilentool, um deine CSV nach
 • Übungsart (exercise)
 • Mindest-RPE (Rate of Perceived Exertion)
zu filtern und das Ergebnis tabellarisch auszugeben.
"""

import argparse           # liest CLI-Argumente
import pandas as pd       # Daten-Framework
import pathlib, sys

# ---------- Hilfsfunktion ---------- #
def load_df() -> pd.DataFrame:
    """CSV laden oder mit klarer Fehlermeldung abbrechen."""
    file = pathlib.Path("app/data/sample_sessions.csv")
    if not file.exists():
        sys.exit("❌  sample_sessions.csv fehlt – erst generate_sample_csv.py ausführen!")
    return pd.read_csv(file, parse_dates=["date"])

# ---------- Hauptfunktion ---------- #
def main():
    parser = argparse.ArgumentParser(
        description="Filtere Trainingseinheiten nach Übung und RPE."
    )
    parser.add_argument("-e", "--exercise", help="Übungsname, z. B. Sprint")
    parser.add_argument("--min_rpe", type=int, default=1,
                        help="nur Einheiten mit RPE ≥ Wert")

    args = parser.parse_args()

    df = load_df()

    # Filter 1: Übung
    if args.exercise:
        df = df[df.exercise == args.exercise]

    # Filter 2: Mindest-RPE
    df = df[df.rpe >= args.min_rpe]

    # Ausgabe
    if df.empty:
        print("⚠️  Keine Zeilen erfüllen die Filter.")
    else:
        print(df.to_string(index=False))

# ---------- Skript-Entry ---------- #
if __name__ == "__main__":
    main()
