import sqlite3

DB_FILEPATH = "www/custom/chores/chores.db"

# Connect to the database (creates a new file if it doesn't exist)
conn = sqlite3.connect(DB_FILEPATH)

# Create the "Chore" table
conn.execute('''
    CREATE TABLE IF NOT EXISTS chore (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        instructions TEXT,        
        type TEXT NOT NULL,
        cycle INTEGER DEFAULT 7,
        weekly_day INTEGER DEFAULT 7,
        monthly_day INTEGER DEFAULT 1,
        yearly_date DATETIME,
        prev_exec INTEGER,
        next_due DATETIME,
        time_estimate INTEGER,
        category TEXT NOT NULL DEFAULT 'house',
        score INTEGER,
        priority INTEGER DEFAULT 5,
        FOREIGN KEY (prev_exec) REFERENCES execution (id)
    )
''')

# Create the "Execution" table
conn.execute('''
    CREATE TABLE IF NOT EXISTS execution (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chore INTEGER NOT NULL,
        timestamp DATETIME NOT NULL,
        days_to_due INTEGER,
        performed_by TEXT,
        time_spent INTEGER,
        comment TEXT,
        score_awarded INTEGER,
        FOREIGN KEY (chore) REFERENCES chore (id)
    )
''')

# Execute the SELECT statement
print("Chore table:")
cursor = conn.execute('SELECT * FROM chore')
rows = cursor.fetchall()
for row in rows:
    print(row)

print("Execution table:")
cursor = conn.execute('SELECT * FROM execution')
rows = cursor.fetchall()
for row in rows:
    print(row)

# Close the connection
conn.close()
