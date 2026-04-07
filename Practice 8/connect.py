import psycopg2
from config import DB_PARAMS

def get_connection():
    """Returns a connection object to the PostgreSQL database."""
    return psycopg2.connect(**DB_PARAMS)
