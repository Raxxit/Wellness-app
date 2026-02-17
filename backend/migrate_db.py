import sqlite3
import os

# Path to your database
db_path = os.path.join('instance', 'wellness.db')

# Connect to database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# List of ALTER commands
alter_commands = [
    "ALTER TABLE Users ADD COLUMN user_type INTEGER DEFAULT 0",
    "ALTER TABLE Users ADD COLUMN related_docs TEXT",
    "ALTER TABLE Users ADD COLUMN bio TEXT",
    "ALTER TABLE Users ADD COLUMN is_verified BOOLEAN DEFAULT 0",
    "ALTER TABLE Users ADD COLUMN created_at DATETIME"
]

# Execute each command
print("Starting database migration...")
for command in alter_commands:
    try:
        cursor.execute(command)
        print(f"✓ Executed: {command}")
    except sqlite3.OperationalError as e:
        print(f"⚠ Skipped (column may exist): {command}")
        print(f"  Error: {e}")

# Commit changes
conn.commit()
conn.close()

print("\n✅ Migration completed successfully!")