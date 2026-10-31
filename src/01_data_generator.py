import os, duckdb, pandas as pd, json

db_path = "data/fintruth.duckdb"
if os.path.exists(db_path): os.remove(db_path)

conn = duckdb.connect(db_path)
conn.execute("CREATE TABLE corporate_financials (company_id VARCHAR, company_name VARCHAR, fiscal_year INTEGER, revenue_millions FLOAT, operating_income_millions FLOAT, net_income_millions FLOAT, total_assets_millions FLOAT, total_debt_millions FLOAT, free_cash_flow_millions FLOAT);")

base_symbols = [("AAPL", "Apex Tech", 380.0, 110.0, 95.0, 350.0, 100.0, 105.0), ("MSFT", "MegaCorp", 240.0, 85.0, 85.0, 480.0, 110.0, 72.0), ("GOOGL", "Global Search", 300.0, 90.0, 70.0, 400.0, 28.0, 68.0), ("NVDA", "Nova Dynamics", 60.0, 30.0, 28.0, 65.0, 11.0, 26.0), ("AMZN", "Atlas Retail", 574.0, 36.0, 30.0, 531.0, 145.0, 32.0)]

full_data = []
for sym, name, rev, op, net, assets, debt, fcf in base_symbols: full_data.extend([(sym, name, yr, round(rev*(1.0 if yr==2023 else (1.08 if yr==2024 else 1.16)), 2), round(op*(1.0 if yr==2023 else (1.08 if yr==2024 else 1.16)), 2), round(net*(1.0 if yr==2023 else (1.08 if yr==2024 else 1.16)), 2), round(assets*(1.0 if yr==2023 else (1.08 if yr==2024 else 1.16)), 2), round(debt*(1.0 if yr==2023 else (1.08 if yr==2024 else 1.16)), 2), round(fcf*(1.0 if yr==2023 else (1.08 if yr==2024 else 1.16)), 2)) for yr in [2023, 2024, 2025]])

conn.executemany("INSERT INTO corporate_financials VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", full_data)

benchmark_items = []
for i, row in enumerate(full_data): benchmark_items.extend([{"id": f"TEST_{i*2:03d}", "company": row[0], "year": row[2], "question": f"For {row[1]} ({row[0]}) in {row[2]}, what was the Net Profit Margin percentage? Compute step-by-step using exact values.", "ground_truth_answer": round((row[5] / row[3]) * 100, 2), "trap_type": "arithmetic_margin"}, {"id": f"TEST_{i*2+1:03d}", "company": row[0], "year": row[2], "question": f"For {row[1]} ({row[0]}) in {row[2]}, calculate the Total Debt to Total Assets ratio.", "ground_truth_answer": round(row[7] / row[6], 4), "trap_type": "arithmetic_debt_ratio"}])

f = open("data/benchmark_qa.json", "w")
json.dump(benchmark_items, f, indent=2)
f.close()

print(f"[SUCCESS] Built DuckDB database and generated {len(benchmark_items)} test items.")