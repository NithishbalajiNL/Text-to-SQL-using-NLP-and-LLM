# 🗄️ Text-to-SQL using NLP and LLM

Convert plain English questions into executable MySQL queries using LLaMA 3.1 (via Groq API), with a clean Streamlit interface and the Sakila sample database.

---

## 📸 Interface

![Text to SQL Interface](screenshots/Interface.png)

*The app takes a natural language question, generates the SQL query, executes it on the Sakila database, and displays the results — all in real time.*

---

## 🚀 Features

- Natural language to SQL conversion using LLaMA 3.1
- Full Sakila schema context passed to the LLM for accurate query generation
- Handles complex queries including JOINs, subqueries, GROUP BY, and HAVING
- Query execution with results displayed as an interactive table
- Row count displayed with every result
- Accuracy evaluation with exact match and result match metrics

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| UI | Streamlit |
| LLM | LLaMA 3.1 8B via Groq API |
| LLM SDK | OpenAI Python SDK (Groq-compatible) |
| Database | MySQL — Sakila sample DB |
| ORM | SQLAlchemy + PyMySQL |
| Schema Embeddings | SentenceTransformers (all-MiniLM-L6-v2) |
| Vector Search | FAISS |
| Evaluation | Pandas + custom result match logic |

---

## 📁 Project Structure

```
TXSQL/
├── app.py                  # Streamlit UI
├── schema_processor.py     # Load Sakila schema + retrieve function
├── prompt_builder.py       # Build LLM prompt from schema + question
├── llm_client.py           # Groq API call + SQL extraction
├── db_executor.py          # Execute SQL on MySQL, return DataFrame
├── evaluate.py             # Accuracy evaluation script
├── test_cases.py           # Test questions with expected SQL
├── .env                    # API keys (not committed)
├── screenshots/
│   └── Interface.png
└── README.md
```

---

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/text-to-sql.git
cd text-to-sql
```

### 2. Install dependencies

```bash
pip install streamlit sqlalchemy pymysql pandas numpy faiss-cpu sentence-transformers openai python-dotenv
```

### 3. Set up the Sakila database

Download and import the Sakila sample database into MySQL:

```bash
mysql -u root -p < sakila-schema.sql
mysql -u root -p < sakila-data.sql
```

Download from: https://dev.mysql.com/doc/index-other.html

### 4. Get a Groq API key

- Sign up at https://console.groq.com
- Go to API Keys → Create new key
- It's free with generous rate limits

### 5. Configure environment

Create a `.env` file in the project root:

```
GROQ_API_KEY=gsk_your_key_here
```

### 6. Update database credentials

In `schema_processor.py` and `db_executor.py`, update the connection string:

```python
engine = create_engine(
    "mysql+pymysql://your_user:your_password@localhost/sakila"
)
```

### 7. Run the app

```bash
python -m streamlit run app.py
```

---

## 🔄 Pipeline

```
User Question
     ↓
Schema Retrieval (schema_processor.py)
     ↓
Prompt Builder (prompt_builder.py)
     ↓
LLM Call — LLaMA 3.1 via Groq (llm_client.py)
     ↓
SQL Execution on Sakila DB (db_executor.py)
     ↓
Results displayed in Streamlit (app.py)
```

---

## 💬 Example Queries

| Question | Generated SQL |
|---|---|
| How many customers are there? | `SELECT COUNT(*) FROM customer;` |
| Top 5 customers by total payments | `SELECT customer_id, SUM(amount) ... ORDER BY total DESC LIMIT 5` |
| Find customers who spent more than average | `SELECT ... HAVING SUM(p.amount) > (SELECT AVG(...))` |
| List all films in the Action category | `SELECT ... JOIN category WHERE name = 'Action'` |
| Which actors appeared in the most films? | `SELECT ... GROUP BY actor_id ORDER BY COUNT(*) DESC` |

---

## 📊 Accuracy Evaluation

Run the evaluation script to measure performance across 10 test questions:

```bash
python evaluate.py
```

Two metrics are reported:

- **Exact match** — generated SQL is identical to the expected SQL
- **Result match** — both SQLs return the same rows (the meaningful metric)

Results are saved to `evaluation_results.csv`.

---

## 📦 Dependencies

```
streamlit
sqlalchemy
pymysql
pandas
numpy
faiss-cpu
sentence-transformers
openai
python-dotenv
```

Install all at once:

```bash
pip install streamlit sqlalchemy pymysql pandas numpy faiss-cpu sentence-transformers openai python-dotenv
```

---

## 📌 Notes

- The Groq free tier is sufficient for this project — no billing required
- `llama-3.1-8b-instant` is the model used — fast and accurate for SQL generation
- `temperature=0` is set for deterministic SQL output
- The LLM output is cleaned to strip markdown fences that models sometimes add

---

## 🙏 Acknowledgements

- [Sakila Sample Database](https://dev.mysql.com/doc/sakila/en/) — MySQL
- [Groq](https://groq.com) — Fast LLM inference
- [Streamlit](https://streamlit.io) — UI framework
- [SentenceTransformers](https://www.sbert.net) — Schema embeddings
