import sqlite3

conn = sqlite3.connect('nakshatras.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS nakshatras (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,  -- Add UNIQUE constraint to avoid duplicates
    star_name TEXT,
    ra REAL,
    dec REAL,
    image_path TEXT
)
''')

print("Database setup complete with image_path column.")

conn.commit()
conn.close()
