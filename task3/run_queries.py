"""
Task 3 - run all 5 SQL files against eklipse.db and print their results.
Also writes each result to results/<name>.csv for the analysis/deck.

Run:  python run_queries.py   (build_database.py must have run first)
"""
import glob
import os
import sqlite3
import pandas as pd

DB_PATH = "eklipse.db"
SQL_DIR = "sql"
OUT_DIR = "results"


def main():
    if not os.path.exists(DB_PATH):
        raise SystemExit("eklipse.db not found - run build_database.py first.")
    os.makedirs(OUT_DIR, exist_ok=True)
    con = sqlite3.connect(DB_PATH)

    for sql_path in sorted(glob.glob(os.path.join(SQL_DIR, "*.sql"))):
        name = os.path.splitext(os.path.basename(sql_path))[0]
        with open(sql_path, "r", encoding="utf-8") as fh:
            query = fh.read()
        print("\n" + "=" * 70)
        print(name)
        print("=" * 70)
        df = pd.read_sql_query(query, con)
        print(df.to_string(index=False))
        df.to_csv(os.path.join(OUT_DIR, f"{name}.csv"), index=False)

    con.close()
    print("\nAll queries executed. Results saved to ./results/")


if __name__ == "__main__":
    main()
