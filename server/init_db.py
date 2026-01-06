import sqlite3

# 1. Connect to the database file
connection = sqlite3.connect('wellness.db')

print("Opened database successfully")

# 2. Create a "Cursor"
cursor = connection.cursor()

# --- TABLE 1: USERS ---
# We delete the table first so we can run this script multiple times to "reset" the DB
connection.execute('DROP TABLE IF EXISTS users')

# Create the table with columns matching your Vue Register form
connection.execute('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

print("Table 'users' created successfully")

# --- (OPTIONAL) TABLE 2: QUESTIONNAIRE ---
# Since you have a questionnaire page, let's prep a table for it
connection.execute('DROP TABLE IF EXISTS questionnaires')

connection.execute('''
    CREATE TABLE questionnaires (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        goal TEXT,
        activity_level TEXT,
        diet_preference TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
''')

print("Table 'questionnaires' created successfully")

# 3. Seed Data (Optional)
# Let's add one "Fake" user just so the DB isn't empty
cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            ('Admin User', 'admin@wellness.com', 'admin123')
            )

print("Added dummy user: admin@wellness.com / admin123")

# 4. Save (Commit) and Close
connection.commit()
connection.close()