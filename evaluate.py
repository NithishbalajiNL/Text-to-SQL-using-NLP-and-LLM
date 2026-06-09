# evaluate.py

import sys
sys.path.insert(0, r"D:\TXSQL")

import pandas as pd
from schema_processor import retrieve_schema
from prompt_builder import build_prompt
from llm_client import get_sql
from db_executor import run_query
from test_cases import test_cases

# ==========================
# EVALUATION METRICS
# ==========================

def normalize(df: pd.DataFrame) -> set:
    return set(
        tuple(row)
        for row in df.values.tolist()
    )

def evaluate():

    total       = len(test_cases)
    exact_match = 0
    result_match = 0
    failed      = 0

    results = []

    for i, tc in enumerate(test_cases):

        question     = tc["question"]
        expected_sql = tc["expected_sql"].strip()

        print(f"\n[{i+1}/{total}] {question}")

        # ==========================
        # GENERATE SQL
        # ==========================

        schema = retrieve_schema()
        prompt = build_prompt(schema, question)
        generated_sql = get_sql(prompt)

        print(f"  Generated : {generated_sql}")
        print(f"  Expected  : {expected_sql}")

        # ==========================
        # EXACT MATCH
        # ==========================

        is_exact = (
            generated_sql.strip().lower() ==
            expected_sql.strip().lower()
        )

        # ==========================
        # RESULT MATCH
        # ==========================

        expected_df  = run_query(expected_sql)
        generated_df = run_query(generated_sql)

        if "error" in generated_df.columns:
            is_result_match = False
            failed += 1
            print(f"  ERROR: {generated_df['error'][0]}")
        else:
            is_result_match = (
                normalize(expected_df) ==
                normalize(generated_df)
            )

        if is_exact:
            exact_match += 1
        if is_result_match:
            result_match += 1

        results.append({
            "question"      : question,
            "generated_sql" : generated_sql,
            "expected_sql"  : expected_sql,
            "exact_match"   : is_exact,
            "result_match"  : is_result_match,
        })

        print(f"  Exact match : {is_exact}")
        print(f"  Result match: {is_result_match}")

    # ==========================
    # SUMMARY
    # ==========================

    print("\n" + "="*50)
    print(f"Total Questions : {total}")
    print(f"Exact Match     : {exact_match}/{total} ({exact_match/total*100:.1f}%)")
    print(f"Result Match    : {result_match}/{total} ({result_match/total*100:.1f}%)")
    print(f"Failed (errors) : {failed}/{total}")
    print("="*50)

    # ==========================
    # SAVE RESULTS
    # ==========================

    df = pd.DataFrame(results)
    df.to_csv("evaluation_results.csv", index=False)
    print("\nSaved to evaluation_results.csv")


if __name__ == "__main__":
    evaluate()