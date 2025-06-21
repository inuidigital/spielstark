import sqlite3, pathlib

# Pfad: app/data/spielstark.db
db_path = pathlib.Path("app/data/spielstark.db")
db_path.parent.mkdir(parents=True, exist_ok=True)   # Ordner sicherstellen

con = sqlite3.connect(db_path)
cur = con.cursor()

# Tabelle mood_log anlegen, falls sie noch nicht existiert
cur.execute("""
CREATE TABLE IF NOT EXISTS mood_log (
    id     INTEGER PRIMARY KEY AUTOINCREMENT,
    date   TEXT    NOT NULL,
    player TEXT    NOT NULL,
    mood   INTEGER CHECK(mood BETWEEN 1 AND 10)
);
""")

con.commit()
con.close()
print(f"✔️  DB & Tabelle mood_log bereit unter {db_path}")
