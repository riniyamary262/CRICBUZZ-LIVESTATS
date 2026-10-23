import sqlite3
from contextlib import contextmanager

DB_PATH = "cricket.db"

@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def init_db():
    with get_db() as conn:
        cur = conn.cursor()
        cur.executescript("""
        CREATE TABLE IF NOT EXISTS players (
            player_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            country TEXT,
            role TEXT,
            batting_style TEXT,
            bowling_style TEXT
        );
        CREATE TABLE IF NOT EXISTS venues (
            venue_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            city TEXT,
            country TEXT,
            capacity INTEGER
        );
        CREATE TABLE IF NOT EXISTS matches (
            match_id INTEGER PRIMARY KEY,
            description TEXT,
            team1 TEXT,
            team2 TEXT,
            venue_id INTEGER,
            match_date TEXT,
            winner TEXT,
            victory_margin TEXT,
            victory_type TEXT,
            toss_winner TEXT,
            toss_decision TEXT,
            FOREIGN KEY (venue_id) REFERENCES venues(venue_id)
        );
        CREATE TABLE IF NOT EXISTS player_stats (
            stat_id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id INTEGER,
            match_id INTEGER,
            format TEXT,
            runs INTEGER DEFAULT 0,
            balls_faced INTEGER DEFAULT 0,
            wickets INTEGER DEFAULT 0,
            overs_bowled REAL DEFAULT 0,
            runs_conceded INTEGER DEFAULT 0,
            catches INTEGER DEFAULT 0,
            stumpings INTEGER DEFAULT 0,
            FOREIGN KEY (player_id) REFERENCES players(player_id),
            FOREIGN KEY (match_id) REFERENCES matches(match_id)
        );
        """)

    seed_sample_data()


def seed_sample_data():
    with get_db() as conn:
        cur = conn.cursor()

        # Venues
        cur.executemany("INSERT OR IGNORE INTO venues VALUES (?,?,?,?,?)", [
            (1, "Wankhede Stadium", "Mumbai", "India", 33000),
            (2, "MCG", "Melbourne", "Australia", 100024),
            (3, "Lord's", "London", "England", 30000),
        ])

        # Players
        cur.executemany("INSERT OR IGNORE INTO players VALUES (?,?,?,?,?,?)", [
            (1, "Virat Kohli", "India", "Batsman", "Right", "Right medium"),
            (2, "Rohit Sharma", "India", "Batsman", "Right", "Right off-break"),
            (3, "Jasprit Bumrah", "India", "Bowler", "Right", "Right fast"),
            (4, "Steve Smith", "Australia", "Batsman", "Right", "Right leg-break"),
        ])

        # Matches
        cur.executemany("INSERT OR IGNORE INTO matches VALUES (?,?,?,?,?,?,?,?,?,?,?)", [
            (101, "India vs Australia", "India", "Australia", 1, "2025-01-15", "India", "5 wickets", "wickets", "India", "bat"),
            (102, "England vs India", "England", "India", 3, "2025-02-10", "England", "30 runs", "runs", "India", "bowl"),
        ])

        # Stats
        cur.executemany("""INSERT OR IGNORE INTO player_stats
            (player_id,match_id,format,runs,balls_faced,wickets,overs_bowled,runs_conceded,catches,stumpings)
            VALUES (?,?,?,?,?,?,?,?,?,?)""", [
            (1, 101, "ODI", 85, 90, 0, 0, 0, 1, 0),
            (2, 101, "ODI", 60, 55, 0, 0, 0, 0, 0),
            (3, 101, "ODI", 5, 10, 3, 10, 45, 0, 0),
            (1, 102, "Test", 120, 200, 0, 0, 0, 2, 0),
        ])
