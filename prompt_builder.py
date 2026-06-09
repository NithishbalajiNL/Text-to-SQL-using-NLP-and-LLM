# prompt_builder.py

# ==========================
# BUILD PROMPT
# ==========================

def build_prompt(schema_context: str, question: str) -> str:

    return f"""You are a MySQL expert working with the Sakila database.
Given the table schema below, write a single valid MySQL query to answer the question.

Schema:
{schema_context}

Question: {question}

Rules:
- Return ONLY the SQL query
- No explanation, no markdown, no backticks
- Use only the tables and columns provided in the schema
"""