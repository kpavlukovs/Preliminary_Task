# Preliminary_Task
## Part 2
### SQL Injection in search_documents() and in save_answer().
What’s wrong:
The code builds SQL using string concatenation: "WHERE content LIKE '%" + question + "%'" and "VALUES ('" + question + "', '" + answer + "')"

Why it matters:
A user can inject SQL and modify or destroy data

Fix:
cursor.execute("SELECT id, title, content FROM documents WHERE content LIKE ?", (f"%{question}%",))
conn.execute("INSERT INTO answers (question, answer) VALUES (?, ?)", (question, answer))
### Hard‑coded API key
What’s wrong:
API_KEY = "sk-prod-abc123xyz", API key is stored directly in source code

Why it matters:
Keys may leak through GitHub, logs and can be abused to run up costs or steal data

Fix:
import os
API_KEY = os.getenv("API_KEY")
### LLM Called Twice
What’s wrong:
print(ask_llm(q, docs))
save_answer(q, ask_llm(q, docs))
calls the API two times.

Why it matters:
Doubles API cost, latency, and may return inconsistent answers.

Fix:
answer = ask_llm(q, docs)
print(answer)
save_answer(q, answer)

### No Error Handling for API Requests
What’s wrong:
Assumes this request always succeeds: response.json()["response"]

Why it matters:
Crashes on timeouts, invalid JSON, or API failures.

Fix:
response.raise_for_status()

try:
    r = response.json()
except ValueError:
    raise RuntimeError("Invalid JSON from LLM")

if "error" in r:
    raise RuntimeError(r["error"])

if not r.get("response"):
    raise RuntimeError("Empty LLM response")

return r["response"]

## Part 3
### Q1
The first thing to break is the LIKE '%...%' query because it forces a full table scan, which becomes very slow at 1M rows. Postgres indexes cannot be used efficiently with a leading wildcard. I would switch to Full Text Search (tsvector + GIN index).
### Q2
Sending all documents to the LLM causes large prompts, high cost, and context window limits. RAG setup fixes this by splitting documents into small chunks, embedding each chunk, and retrieving only the top‑k most relevant chunks for the prompt.
### Q3
An LLM API can fail due to network errors or timeouts, invalid responses, or rate limits (429). Network issues I would handle with retries and timeouts. JSON I would validate response integrity and implement backoff.
