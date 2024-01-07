import sqlite3

# Connect to the database (creates a new file if it doesn't exist)
conn = sqlite3.connect('chores.db')

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
        score_awarded INTEGER,
        FOREIGN KEY (chore) REFERENCES chore (id)
    )
''')

# Execute the SELECT statement
cursor = conn.execute('SELECT * FROM chore')

# Fetch all rows from the cursor
rows = cursor.fetchall()

# Print the rows
for row in rows:
    print(row)

# Close the connection
conn.close()
