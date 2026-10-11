# Game Library API

A simple REST API for managing a video game library, built with Python, FastAPI, and SQLite.

## Features

- Retrieve all games
- Retrieve a game by ID
- Add a new game
- Replace a game's information using PUT
- Update selected fields using PATCH
- Delete a game
- Store game data persistently in SQLite
- Handle errors for games that do not exist

## Technologies

- Python
- FastAPI
- Pydantic
- SQLite

## Installation

1. Clone or download this repository.
2. Create and activate a Python virtual environment.
3. Install the dependencies:

   `pip install fastapi uvicorn`

4. Initialize the database:

   `python database.py`

5. Start the API:

   `uvicorn main:app --reload`

## API Documentation

After starting the server, open:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Project Structure

- `main.py` — API routes and request models
- `database.py` — SQLite connection and database initialization
- `games.db` — Local SQLite database, generated when the database is initialized

## Learning Goals

This project was built to practice REST APIs, CRUD operations, request validation, error handling, and database integration.
