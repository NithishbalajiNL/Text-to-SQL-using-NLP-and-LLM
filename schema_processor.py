# schema_processor.py

import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sqlalchemy import create_engine

# ==========================
# MYSQL CONNECTION
# ==========================

engine = create_engine(
    "mysql+pymysql://root:Nithishbalaji%407944@localhost/sakila"
)

# ==========================
# LOAD SCHEMA
# ==========================

query = """
SELECT
    TABLE_NAME,
    COLUMN_NAME
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'sakila'
"""

schema_df = pd.read_sql(query, engine)

# ==========================
# CREATE SCHEMA DOCUMENTS
# ==========================

schema_docs = []

for table in schema_df["TABLE_NAME"].unique():

    columns = schema_df[
        schema_df["TABLE_NAME"] == table
    ]["COLUMN_NAME"].tolist()

    doc = f"Table: {table} | Columns: {', '.join(columns)}"

    schema_docs.append(doc)

# ==========================
# FULL SCHEMA STRING
# ==========================

def retrieve_schema(question: str = None) -> str:
    return "\n".join(schema_docs)

# RUN ONLY WHEN DIRECT
# ==========================

if __name__ == "__main__":
    print("Schema Loaded:", len(schema_docs), "tables")
    print(retrieve_schema())