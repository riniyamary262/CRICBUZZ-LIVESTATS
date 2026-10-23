from utils.db_connection import get_db

def create_player(name, country, role, batting, bowling):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO players (name,country,role,batting_style,bowling_style) VALUES (?,?,?,?,?)",
                    (name, country, role, batting, bowling))
        return cur.lastrowid

def get_all_players():
    with get_db() as conn:
        return [dict(r) for r in conn.execute("SELECT * FROM players").fetchall()]

def update_player(pid, name, country, role):
    with get_db() as conn:
        conn.execute("UPDATE players SET name=?,country=?,role=? WHERE player_id=?",
                     (name, country, role, pid))

def delete_player(pid):
    with get_db() as conn:
        conn.execute("DELETE FROM players WHERE player_id=?", (pid,))