from typing import List
from fastapi import FastAPI, Path, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import contextmanager
from pathlib import Path

import sqlite3
import logging
import os

from backend.database.models import User, Repository

# Name of the database we use
DB_NAME = os.path.join(os.getcwd(), "backend", "database", "github.db")

logger = logging.getLogger("uvicorn.error")
logger.setLevel(logging.INFO)


@contextmanager
def get_cursor() -> sqlite3.Cursor:
    """Get a cursor to the sqllite db within a contex manager"""
    con = sqlite3.connect(DB_NAME)
    curs = con.cursor()
    try:
        yield curs
    finally:
        curs.close()
        con.commit()
        con.close()


app = FastAPI(debug=True)

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def setup_db() -> None:
    """Create database, if needed."""
    if not Path(DB_NAME).exists():
        logger.info(f"Creating database {DB_NAME}")
        with get_cursor() as cur:
            # Create tables
            cur.execute(
                "CREATE TABLE Users(user_id INTEGER PRIMARY KEY, username TEXT NOT NULL UNIQUE)"
            )
            cur.execute(
                "CREATE TABLE Repositories(repo_id INTEGER PRIMARY KEY, name TEXT NOT NULL, url TEXT NOT NULL, repo_owner INTEGER, FOREIGN KEY(repo_owner) REFERENCES Users(user_id))"
            )
            # Example data
            cur.execute('INSERT INTO Users VALUES(61523648, "jlcowles")')
            cur.execute(
                'INSERT INTO Repositories VALUES(272178507, "readme-best-practices", "https://github.com/jlcowles/readme-best-practices", 61523648)'
            )    
    else:
        logger.info(f"Database {DB_NAME} already exists. Delete {DB_NAME} to start over.")
    


@app.get("/users", response_model=List[User])
async def get_users() -> List[User]:
    """Get all users"""
    ret_list = []
    with get_cursor() as cur:
        for row in cur.execute("SELECT * FROM Users"):
            ret_list.append(User(user_id=row[0], username=row[1]))
    if len(ret_list) > 0:
        return ret_list
    raise HTTPException(status_code=404, detail="No Users found")


@app.get("/users/{username}", response_model=User)
async def get_user(
    username: str = Path(title="The username of the user to get"),
) -> User:
    """Get a specific user"""
    with get_cursor() as cur:
        res = cur.execute("SELECT * FROM Users WHERE username = ?", (username,))
        ret = res.fetchone()
        if ret:
            usr = User(user_id=ret[0], username=ret[1])
            return usr

    raise HTTPException(status_code=404, detail="User not found")


@app.get("/repos", response_model=List[Repository])
async def get_repos() -> List[Repository]:
    """Get all repos"""
    ret_list = []
    with get_cursor() as cur:
        for row in cur.execute("SELECT * FROM Repositories"):
            ret_list.append(
                Repository(repo_id=row[0], name=row[1], url=row[2], repo_owner=row[3])
            )
    if len(ret_list) > 0:
        return ret_list
    raise HTTPException(status_code=404, detail="No Repositories found")


@app.get("/repos/{repo_id}", response_model=Repository)
async def get_repo(
    repo_id: int = Path(title="The ID of the repo to get"),
) -> Repository:
    """Get a specific repo"""
    with get_cursor() as cur:
        res = cur.execute("SELECT * FROM Repositories WHERE repo_id = ?", (repo_id,))
        row = res.fetchone()
        if row:
            repo = Repository(
                repo_id=row[0], name=row[1], url=row[2], repo_owner=row[3]
            )
            return repo

    raise HTTPException(status_code=404, detail="Repository not found")


@app.get("/repos/{username}/repos", response_model=List[Repository])
async def get_repos_for_user(
    username: str = Path(title="The username of the user who's repos you want to get"),
) -> List[Repository]:
    """Get all of the repos for a given user"""
    ret_list = []
    with get_cursor() as cur:
        for row in cur.execute(
            "SELECT repo_id, name, url, repo_owner  FROM Repositories INNER JOIN Users on Repositories.repo_owner = Users.user_id WHERE username = ?",
            (username,),
        ):
            ret_list.append(
                Repository(repo_id=row[0], name=row[1], url=row[2], repo_owner=row[3])
            )
    if len(ret_list) > 0:
        return ret_list
    raise HTTPException(status_code=404, detail="No Repositories found")
