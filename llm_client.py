# llm_client.py

import os
from openai import OpenAI
from dotenv import load_dotenv

# ==========================
import os

client = OpenAI(
    api_key="Your_Key",
    base_url="https://api.groq.com/openai/v1"
)

# GENERATE SQL
# ==========================

def get_sql(prompt: str) -> str:

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "You are a MySQL expert. Return ONLY the SQL query, no explanation, no markdown, no backticks."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    sql = response.choices[0].message.content.strip()

    sql = sql.replace("```sql", "").replace("```", "").strip()

    return sql


if __name__ == "__main__":
    test_prompt = "List all customers from the customer table."
    print("Generated SQL:\n", get_sql(test_prompt))