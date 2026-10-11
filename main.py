

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from database import get_connection

app = FastAPI()



# Model for incoming game data
class GameCreate(BaseModel):
    title : str
    release_year : int
    genre : str

class GameUpdate(BaseModel):
    title: str | None = None
    release_year: int | None = None
    genre: str | None = None

@app.get("/")
def home():
    return {"message": "Hello, FastAPI!"}


@app.get("/games/")
def get_games():
    connection = get_connection()

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM games")
        results = cursor.fetchall()

        return [dict(game) for game in results]

    finally:
        connection.close()


@app.get("/games/{game_id}")
def get_game(game_id: int):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM games WHERE id = ?", (game_id,))

        game = cursor.fetchone()

        if game is None:
            raise HTTPException(status_code=404, detail="Game not found")

        return dict(game)

    finally:
        connection.close()


@app.get("/about")
def about():
    return{'project': 'Game Library API', 'version': '1.0.0'}


@app.post("/games/", status_code=status.HTTP_201_CREATED)
def create_game(game: GameCreate):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO games (title, release_year, genre)
            VALUES (?, ?, ?)
            """,
            (game.title, game.release_year, game.genre)
        )

        connection.commit()

        new_game_id = cursor.lastrowid

        cursor.execute(
            "SELECT * FROM games WHERE id = ?",
            (new_game_id,)
        )

        new_game = cursor.fetchone()

        return dict(new_game)

    finally:
        connection.close()


@app.put("/games/{game_id}")
def update_game(game_id: int, updated_game: GameCreate):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("SELECT id FROM games WHERE id = ?", (game_id,))

        game = cursor.fetchone()

        if game is None:
            raise HTTPException(status_code=404, detail="Game not found")

        cursor.execute(
            """
            UPDATE games
            SET title = ?, release_year = ?, genre = ?
            WHERE id = ?
            """,
            (
                updated_game.title,
                updated_game.release_year,
                updated_game.genre,
                game_id,
            ),
        )

        connection.commit()

        cursor.execute("SELECT * FROM games WHERE id = ?", (game_id,))

        updated_record = cursor.fetchone()

        return dict(updated_record)

    finally:
        connection.close()


@app.delete("/games/{game_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_game(game_id: int):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("DELETE FROM games WHERE id = ?", (game_id,))

        deleted_count = cursor.rowcount

        if deleted_count == 0:
            raise HTTPException(status_code=404, detail="Game not found")

        connection.commit()

        return None

    finally:
        connection.close()


@app.patch('/games/{game_id}')
def patch_game(game_id:int, updated_game:GameUpdate):
    changes = updated_game.model_dump(exclude_unset=True)

    if not changes:
        raise HTTPException(status_code=404, detail="No fields provided ")

    connection = get_connection()
    try:
        cursor = connection.cursor()

        cursor.execute("SELECT id FROM games WHERE id = ?", (game_id,))



        if cursor.fetchone() is None:
            raise HTTPException(status_code=404, detail="Game not found")

        set_clause = ", ".join(f"{field} = ?" for field in changes)

        values = list(changes.values()) + [game_id]

        cursor.execute(f"UPDATE games SET {set_clause} WHERE id = ?", values)

        changes = updated_game.model_dump(exclude_unset=True)

        connection.commit()

        cursor.execute("SELECT * FROM games WHERE id = ?", (game_id,))

        updated_record = cursor.fetchone()

        return dict(updated_record)

    finally:
        connection.close()


