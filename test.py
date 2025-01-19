import sqlite3

def remove_duplicates():
    conn = sqlite3.connect('nakshatras.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        DELETE FROM nakshatras
        WHERE id NOT IN (
            SELECT MIN(id)
            FROM nakshatras
            GROUP BY name
        );
    ''')
    
    
    cursor.execute('SELECT * FROM nakshatras;')
    rows = cursor.fetchall()
    
    print("Entries after removing duplicates:")
    for row in rows:
        print(row)
    
    conn.close()

remove_duplicates()
