# LLM Data Agent

> A lightweight LLM-powered data analysis agent built with Python.

基于 Python 与大语言模型（LLM）开发的轻量级智能数据分析 Agent。项目实现了自然语言查询数据库、SQL 自动生成、SQL 自动纠错及 CSV 数据分析等功能，帮助用户无需手写 SQL 即可完成数据查询与分析。

---

## ✨ Features

### 🔹 Natural Language to SQL

支持用户使用自然语言描述查询需求，由大语言模型自动生成 SQL 语句，实现数据库查询。

### 🔹 Metadata Retrieval

根据用户问题动态筛选相关数据表，仅向模型提供目标表结构（DDL），减少无关上下文，提高 SQL 生成效率。

### 🔹 SQL Self-Correction

当生成的 SQL 执行失败时，自动捕获数据库异常信息，并反馈给模型重新生成 SQL，形成"生成 → 执行 → 报错 → 修正"的闭环流程。

### 🔹 SQL Safety Validation

对 SQL 语句进行安全校验，拦截 DELETE、UPDATE、DROP 等危险操作，仅允许执行只读查询。

### 🔹 CSV Data Analysis

支持基于 Pandas 对 CSV 数据进行统计分析，根据自然语言需求生成分析结果。

---

## 🛠 Tech Stack

- Python
- MySQL / SQLite
- Pandas
- DeepSeek API
- Prompt Engineering
- Function Calling

---

## 📌 Workflow

```text
User Question
        │
        ▼
Metadata Retrieval
        │
        ▼
LLM Generate SQL
        │
        ▼
SQL Safety Validation
        │
        ▼
Execute SQL
        │
 ┌──────┴──────┐
 │             │
Success      Failed
 │             │
 ▼             ▼
Result   Error Feedback
               │
               ▼
        Regenerate SQL
```

---

## 📂 Project Structure

```text
llm-data-agent/
│
├── config/
│   ├── llm_config.py
│   └── db_config.py
│
├── core/
│   ├── agent.py
│   ├── metadata_router.py
│   ├── sql_generator.py
│   ├── sql_validator.py
│   └── self_correct.py
│
├── database/
│   ├── sales.db
│   └── schema_dict.json
│
├── utils/
│   └── sql_executor.py
│
├── requirements.txt
├── README.md
└── main.py
```

---

## 🚀 Getting Started

### Clone Repository

```bash
git clone https://github.com/yourname/llm-data-agent.git
cd llm-data-agent
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure API

在 `config/` 目录下创建 `llm_config.py`，配置 DeepSeek API Key。

```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_API_KEY",
    base_url="https://api.deepseek.com"
)
```

### Run

```bash
python main.py
```

---

## 📖 Future Improvements

- 引入向量数据库（FAISS）实现更高效的元数据检索
- 支持多轮对话上下文管理
- 支持更多数据库（PostgreSQL、SQL Server 等）
- 增加 Web UI
- 支持数据可视化图表生成

---

## 📄 License

MIT License

## Demo

**User**

```
查询消费金额最高的前10位用户
```

↓

**Generated SQL**

```sql
SELECT customer_name,
       SUM(amount) AS total_amount
FROM orders
GROUP BY customer_name
ORDER BY total_amount DESC
LIMIT 10;
```

↓

**Result**

| Customer | Amount |
|----------|--------|
| Alice | 12580 |
| Bob | 11800 |