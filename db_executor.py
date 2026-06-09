# db_executor.py

import pandas as pd
from sqlalchemy import create_engine, text

# ==========================
# MYSQL CONNECTION
# ==========================

engine = create_engine(
    "mysql+pymysql://root:Nithishbalaji%407944@localhost/sakila"
)

# ==========================
# EXECUTE SQL
# ==========================

def run_query(sql: str) -> pd.DataFrame:

    try:
        with engine.connect() as conn:
            result = conn.execute(text(sql))
            df = pd.DataFrame(
                result.fetchall(),
                columns=result.keys()
            )
        return df

    except Exception as e:
        return pd.DataFrame({"error": [str(e)]})