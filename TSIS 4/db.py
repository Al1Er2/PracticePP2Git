import psycopg
from config import DB_CONFIG

def get_connection():
    return psycopg.connect(**DB_CONFIG)

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS players (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS game_sessions (
            id SERIAL PRIMARY KEY,
            player_id INTEGER REFERENCES players(id),
            score INTEGER NOT NULL,
            level_reached INTEGER NOT NULL,
            played_at TIMESTAMP DEFAULT NOW()
        );
    """)

    conn.commit()
    cur.close()
    conn.close()

def get_or_create_player(username):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id FROM players WHERE username = %s", (username,))
    player = cur.fetchone()

    if player:
        player_id = player[0]
    else:
        cur.execute(
            "INSERT INTO players(username) VALUES(%s) RETURNING id",
            (username,)
        )
        player_id = cur.fetchone()[0]
        conn.commit()

    cur.close()
    conn.close()
    return player_id

def save_result(username, score, level):
    player_id = get_or_create_player(username)

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO game_sessions(player_id, score, level_reached)
        VALUES(%s, %s, %s)
    """, (player_id, score, level))

    conn.commit()
    cur.close()
    conn.close()

def get_personal_best(username):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT MAX(gs.score)
        FROM game_sessions gs
        JOIN players p ON p.id = gs.player_id
        WHERE p.username = %s
    """, (username,))

    result = cur.fetchone()[0]

    cur.close()
    conn.close()

    return result if result else 0

def get_top_scores():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT p.username, gs.score, gs.level_reached, gs.played_at
        FROM game_sessions gs
        JOIN players p ON p.id = gs.player_id
        ORDER BY gs.score DESC, gs.level_reached DESC
        LIMIT 10
    """)

    results = cur.fetchall()

    cur.close()
    conn.close()

    return results
