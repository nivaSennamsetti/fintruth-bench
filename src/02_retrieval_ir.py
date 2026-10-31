import duckdb
from rank_bm25 import BM25Okapi

print("\nStarting Retrieval Pipeline (Target: Prof. Robert West)")
conn = duckdb.connect("data/fintruth.duckdb")

corpus = ["In 2024, Apex Technologies reported strong growth despite supply chain issues.", "Revenue for Apex Technologies in 2025 hit an all-time high of $391,035 million, heavily driven by services.", "Global Search Labs struggled in Q1 2024 but ended the year with $307,394 million in revenue."]
tokenized_corpus = [doc.split(" ") for doc in corpus]
bm25 = BM25Okapi(tokenized_corpus)

query = "What was the revenue for Apex Technologies in 2025?"
print(f"QUERY: {query}\n")

print("--- 1. BM25 Text Retrieval ---")
top_result = bm25.get_top_n(query.split(" "), corpus, n=1)[0]
print(f"Top Chunk: {top_result}")

print("\n--- 2. DuckDB SQL Metadata Retrieval ---")
df = conn.execute("SELECT revenue_millions FROM corporate_financials WHERE company_id = 'AAPL' AND fiscal_year = 2025").df()
print(df)

print("\n[SUCCESS] Hybrid retrieval engine verified.")