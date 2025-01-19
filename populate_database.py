import sqlite3

# Connect to the database
conn = sqlite3.connect('nakshatras.db')
cursor = conn.cursor()

nakshatras = [
    ('Ashwini', 'Beta Arietis', 1.9, 19.3, 'images/ashwini.jpg'),
    ('Bharani', '41 Arietis', 3.2, 19.7, 'images/bharani.jpg'),
    ('Krittika', 'Eta Tauri', 3.8, 24.1, 'images/krittika.jpg'),
    ('Rohini', 'Aldebaran', 4.6, 16.5, 'images/rohini.jpg'),
    ('MrigaShira', 'Lambda Orionis', 5.6, 9.9, 'images/mrigashira.jpg'),
    ('Ardra', 'Betelgeuse', 5.9, 7.4, 'images/ardra.jpg'),
    ('Punarvasu', 'Castor', 7.6, 31.9, 'images/punarvasu.jpg'),
    ('Pushya', 'Delta Cancri', 8.7, 18.2, 'images/pushya.jpg'),
    ('Ashlesha', 'Alpha Hydrae', 9.5, -8.7, 'images/ashlesha.jpg'),
    ('Magha', 'Regulus', 10.1, 12.0, 'images/magha.jpg')
]

cursor.executemany('''
INSERT INTO nakshatras (name, star_name, ra, dec, image_path)
VALUES (?, ?, ?, ?, ?)
''', nakshatras)

conn.commit()
conn.close()
