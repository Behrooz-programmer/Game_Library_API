import sqlite3


def get_connection():
    connection = sqlite3.connect("games.db")
    connection.row_factory = sqlite3.Row
    return connection


connection = get_connection()
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS games (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    release_year INTEGER NOT NULL,
    genre TEXT NOT NULL
)
""")

cursor.execute("SELECT COUNT(*) FROM games")
game_count = cursor.fetchone()[0]

if game_count == 0:
    games = [
        ("Dark Souls", 2011, "Action RPG"),
        ("Sekiro", 2019, "Action"),
        ("Elden Ring", 2022, "Action RPG"),
    ]

    cursor.executemany(
        """
        INSERT INTO games (title, release_year, genre)
        VALUES (?, ?, ?)
    """,
        games,
    )

    connection.commit()

print("Database is ready!")

connection.close()
