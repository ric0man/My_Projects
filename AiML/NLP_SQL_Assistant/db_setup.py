import sqlite3

conn = sqlite3.connect("data/sample.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY,
    name TEXT,
    department TEXT,
    join_date TEXT
)
""")

cursor.executemany("""
INSERT INTO employees (name, department, join_date) VALUES (?, ?, ?)
""", [
    ("Rohan Gupta", "Engineering", "2021-06-15"),
    ("Aisha Verma", "Marketing", "2020-03-22"),
    ("Kunal Singh", "Finance", "2022-01-10")
])

conn.commit()
conn.close()
