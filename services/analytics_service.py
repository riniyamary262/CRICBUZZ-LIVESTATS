from utils.db_connection import get_db
import pandas as pd
from sql.queries import QUERIES

def run_query(qid, custom_sql=None):
    sql = custom_sql if custom_sql else QUERIES.get(qid, {}).get("sql")
    if not sql:
        return None, "Query not found"
    try:
        with get_db() as conn:
            df = pd.read_sql_query(sql, conn)
        return df, None
    except Exception as e:
        return None, str(e)

def get_query_meta(qid):
    return QUERIES.get(qid, {})
