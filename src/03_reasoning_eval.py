import json, ollama, duckdb

print("Starting Local AI Reasoning Evaluation (Target: Prof. Antoine Bosselut)")
conn = duckdb.connect("data/fintruth.duckdb")
f = open("data/benchmark_qa.json", "r")
benchmark_items = json.load(f)[:2]
f.close()

def eval_item(item, c):
    print(f"\nEvaluating Item: {item['id']}")
    print(f"Question: {item['question']}")
    df = c.execute(f"SELECT * FROM corporate_financials WHERE company_id = '{item['company']}' AND fiscal_year = {item['year']}").df()
    context = df.to_csv(index=False)
    prompt = f"Using this financial data:\n{context}\n\nAnswer the following question. ONLY output the final numerical answer.\nQuestion: {item['question']}"
    response = ollama.chat(model='llama3.2', messages=[{'role': 'user', 'content': prompt}])
    ai_answer = response['message']['content'].strip()
    print(f"Ground Truth: {item['ground_truth_answer']}")
    print(f"Llama 3.2 Output: {ai_answer}")
    print("Match: ", str(item['ground_truth_answer']) in ai_answer)

list(map(lambda x: eval_item(x, conn), benchmark_items))

print("\n[SUCCESS] Local Llama 3.2 Reasoning Evaluated.")