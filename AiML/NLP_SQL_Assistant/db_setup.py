import os
import sqlite3

# Project root: C:\Users\rohan\Desktop\Job\Projects\AiML\NLP_SQL_Assistant
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)  # ensure data/ exists

DB_FILE = os.path.join(DATA_DIR, "sample.db")

# Recreate table for a clean setup (optional: drop if exists)
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY,
    name TEXT,
    department TEXT,
    hire_date TEXT
)
""")

# Clear existing rows to avoid duplicates when re-running setup
cursor.execute("DELETE FROM employees")

cursor.executemany(
    """
    INSERT INTO employees (name, department, hire_date)
    VALUES (?, ?, ?)
    """,
    [
        ("Rohan Gupta", "Engineering", "2021-06-15"),
        ("Aisha Verma", "Marketing", "2020-03-22"),
        ("Kunal Singh", "Finance", "2022-01-10"),
        ("Neha Sharma", "Engineering", "2023-04-01"),
        ("Vikram Mehta", "Finance", "2019-11-12"),
        ("Priya Iyer", "Marketing", "2022-07-19"),
        ("Arjun Rao", "Engineering", "2020-09-05"),
        ("Simran Kaur", "HR", "2021-01-20"),
        ("Rahul Jain", "Finance", "2023-02-14"),
        ("Ananya Bose", "HR", "2018-08-30"),
    ],
)

conn.commit()
conn.close()
