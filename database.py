import sqlite3

DB_NAME = "career.db"


def create_tables():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    # Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        education TEXT,
        skills TEXT,
        mbti TEXT
    )
    """)

    # Career Session Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sessions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        interests TEXT,
        mbti TEXT,
        recommendations TEXT,
        gpt_advice TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def save_user(name, education, skills, mbti):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO users
        (name, education, skills, mbti)
        VALUES (?, ?, ?, ?)
        """,
        (name, education, skills, mbti)
    )

    conn.commit()
    conn.close()


def get_all_users():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")

    rows = cursor.fetchall()

    conn.close()

    return rows


def save_session(
    username,
    interests,
    mbti,
    recommendations,
    gpt_advice
    
):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO sessions
        (
            username,
            interests,
            mbti,
            recommendations,
            gpt_advice
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            username,
            interests,
            mbti,
            recommendations,
            gpt_advice
        )
    )

    conn.commit()
    conn.close()


def get_sessions():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM sessions
    ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows