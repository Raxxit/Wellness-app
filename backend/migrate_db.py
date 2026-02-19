import sqlite3
import os

# Path to your database
db_path = os.path.join('instance', 'wellness.db')

# Connect to database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# List of ALTER commands
alter_commands = [



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