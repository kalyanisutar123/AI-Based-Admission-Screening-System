import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "admission.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Students predictions table
    c.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            gender TEXT,
            marks_10 REAL,
            marks_12 REAL,
            entrance_score REAL,
            preferred_course TEXT,
            composite_score REAL,
            prediction TEXT,
            recommended_college TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Users table for login
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'student',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Insert default admin user (password: admin123)
    import hashlib
    admin_pass = hashlib.sha256("admin123".encode()).hexdigest()
    student_pass = hashlib.sha256("student123".encode()).hexdigest()

    c.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)",
              ("admin", admin_pass, "admin"))
    c.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)",
              ("student", student_pass, "student"))

    conn.commit()
    conn.close()
    print(f"  Database initialized at {DB_PATH}")
    print("  Default users: admin/admin123 and student/student123")

if __name__ == "__main__":
    init_db()