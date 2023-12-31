import sqlite3

def create_database():
    conn = sqlite3.connect('history.db')
    cursor = conn.cursor()

    create_table_query = '''
    CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY,
    role TEXT CHECK(role IN ('user', 'assistant')),
    content TEXT
    )
    '''
    cursor.execute(create_table_query)
    conn.commit()
    conn.close()

# Create the database when the app starts
create_database()