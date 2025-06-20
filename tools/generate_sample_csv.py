import csv, random, datetime as dt, pathlib

# 1) Zielordner app/data/ sicherstellen
path = pathlib.Path("app/data")
path.mkdir(parents=True, exist_ok=True)

# 2) Zieldatei definieren
file = path / "sample_sessions.csv"

# 3) Reproduzierbare Zufallswerte
random.seed(42)
start = dt.date.today() - dt.timedelta(days=30)

with file.open("w", newline="") as f:
    w = csv.writer(f)
    # Kopfzeile
    w.writerow(["date", "exercise", "duration_min", "rpe"])

    # 60 Einträge (= 30 Tage × 2 Sessions)
    for i in range(60):
        w.writerow([
            start + dt.timedelta(days=i // 2),                  # Datum
            random.choice(["Dribbling", "Sprint", "Pass", "Schuss"]),
            random.choice([20, 30, 40, 50]),                    # Minuten
            random.randint(4, 10)                               # RPE 1-10
        ])

print(f"✔️  Wrote {file}")
