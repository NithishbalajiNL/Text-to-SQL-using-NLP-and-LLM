# app.py


# app.py

import sys
import os


sys.path.insert(0, r"D:\TXSQL")

import streamlit as st
from schema_processor import retrieve_schema
from prompt_builder import build_prompt
from llm_client import get_sql
from db_executor import run_query

# ==========================
# PAGE CONFIG
# ==========================

st.set_page_config(
    page_title="Text to SQL",
    page_icon="🗄️",
    layout="wide"
)

# ==========================
# HEADER
# ==========================

st.title("🗄️ Text to SQL")
st.caption("Ask questions about the Sakila database in plain English")

# ==========================
# INPUT
# ==========================
# 
question = st.text_input(
    "Ask a question:",
    placeholder="e.g. List the top 5 customers by total payments"
)

# ==========================
# PIPELINE
# ==========================

if question:

    with st.spinner("Retrieving schema..."):
        schema = retrieve_schema(question)

    with st.spinner("Generating SQL..."):
        prompt = build_prompt(schema, question)
        sql = get_sql(prompt)

    with st.spinner("Running query..."):
        df = run_query(sql)

    # ==========================
    # RESULTS
    # ==========================

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Generated SQL")
        st.code(sql, language="sql")

    with col2:
        st.subheader("Results")
        if "error" in df.columns:
            st.error(df["error"][0])
        else:
            st.success(f"{len(df)} rows returned")
            st.dataframe(df, use_container_width=True)