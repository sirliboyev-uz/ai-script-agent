"""Database migration script to add user_id column."""
import sqlite3
from pathlib import Path

# Database path
db_path = Path(__file__).parent.parent / "data" / "scripts.db"

if not db_path.exists():
    print(f"Database not found at {db_path}")
    print("No migration needed - fresh database will be created with correct schema")
    exit(0)

print(f"Migrating database at {db_path}")

# Connect to database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Check if user_id column exists
    cursor.execute("PRAGMA table_info(scripts)")
    columns = [row[1] for row in cursor.fetchall()]

    if "user_id" in columns:
        print("✅ Database already migrated - user_id column exists")
    else:
        print("Adding user_id column to scripts table...")
        cursor.execute("ALTER TABLE scripts ADD COLUMN user_id INTEGER")
        conn.commit()
        print("✅ Successfully added user_id column")

    # Check if users table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    if cursor.fetchone():
        print("✅ Users table already exists")
    else:
        print("Creating users table...")
        cursor.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email VARCHAR(255) UNIQUE NOT NULL,
                username VARCHAR(100) UNIQUE NOT NULL,
                hashed_password VARCHAR(255) NOT NULL,
                is_active BOOLEAN DEFAULT 1,
                is_superuser BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        print("✅ Successfully created users table")

    print("\n✅ Migration completed successfully!")

except Exception as e:
    print(f"❌ Migration failed: {e}")
    conn.rollback()
    raise

finally:
    conn.close()
