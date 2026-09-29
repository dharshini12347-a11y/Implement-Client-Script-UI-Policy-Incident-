import sqlite3
from pathlib import Path
from contextlib import contextmanager
from .config import get_settings

def db_path():
    url = get_settings().database_url
    if not url.startswith("sqlite:///"):
        raise RuntimeError("This project uses SQLite. Set DATABASE_URL to sqlite:///...")
    return Path(url.replace("sqlite:///", "", 1))

def init_db():
    path = db_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(path) as con:
        con.execute("PRAGMA foreign_keys=ON")
        con.execute("""
        CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            number TEXT NOT NULL UNIQUE,
            caller TEXT NOT NULL,
            category TEXT NOT NULL DEFAULT 'Software',
            subcategory TEXT DEFAULT '',
            short_description TEXT NOT NULL,
            description TEXT DEFAULT '',
            impact TEXT NOT NULL DEFAULT '3',
            urgency TEXT NOT NULL DEFAULT '3',
            assigned_to TEXT DEFAULT '',
            assignment_group TEXT DEFAULT '',
            state TEXT NOT NULL DEFAULT '1',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """)

@contextmanager
def get_db():
    con = sqlite3.connect(db_path())
    con.row_factory = sqlite3.Row
    try:
        yield con
        con.commit()
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()
