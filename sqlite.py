import sqlite3

# Create a connection to the database (or create it if it doesn't exist)
conn = sqlite3.connect('halmstad_temp.db')

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Create a table
cursor.execute('''CREATE TABLE IF NOT EXISTS prev_temps (id INTEGER PRIMARY KEY, name TEXT,celsius text,time text)''')

# Commit and close the connection
conn.commit()
conn.close()