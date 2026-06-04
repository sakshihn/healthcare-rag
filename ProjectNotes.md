# Complete Study Notes — Healthcare RAG Project

### From Python Basics to Production AI — Everything I Built is Explained

---

## HOW TO USE THESE NOTES

Every concept follows this structure:

1. **Plain English** — what it is, no jargon
2. **Real world analogy** — so it sticks forever
3. **Why we used it** — context from your project
4. **The actual code** — exactly what you wrote
5. **Key things to remember** — for interviews

---

# PART 1 — PYTHON FOUNDATIONS

---

## 1.1 Virtual Environment (venv)

### Plain English

A virtual environment is a private, isolated box for your project's Python libraries. Every project gets its own box so libraries don't conflict with each other.

### Analogy

Imagine you have two restaurants. Restaurant A needs ketchup brand X. Restaurant B needs ketchup brand Y. If they share one kitchen, there's a conflict. Virtual environments give each restaurant its own kitchen.

### Why we used it

Our project needed specific versions of libraries (sentence-transformers, chromadb, groq). Without venv, installing these might break other Python projects on your laptop.

### The code

```bash
# Create a virtual environment
python -m venv .venv

# Activate it (Windows)
.venv\Scripts\activate

# Activate it (Mac/Linux)
source .venv/bin/activate

# You know it's active when you see (.venv) at the start of terminal
```

### Key things to remember

- Always activate venv before working on a project
- Never commit the `.venv` folder to GitHub (add it to .gitignore)
- `pip install` inside venv only affects that project, not your whole computer

---

## 1.2 pip + requirements.txt

### Plain English

`pip` is Python's package installer. `requirements.txt` is a shopping list of all the libraries your project needs.

### Analogy

`pip install` is ordering from Amazon. `requirements.txt` is your saved shopping list. Anyone can take your list and order exactly the same things.

### The code

```bash
# Install a library
pip install streamlit

# Save all installed libraries to a file
pip freeze > requirements.txt

# Install everything from the list (on another computer)
pip install -r requirements.txt
```

### Key things to remember

- Always run `pip freeze > requirements.txt` after installing new libraries
- This file is how Streamlit Cloud and Docker know what to install
- `pip freeze` shows ALL libraries including dependencies — that's why the list gets long

---

## 1.3 .env + python-dotenv

### Plain English

A `.env` file stores secret values like API keys outside your code. The `python-dotenv` library reads that file and makes those values available to your Python code.

### Analogy

Your house key is secret. You don't tape it to your front door (that's posting API keys on GitHub). You keep it in your pocket (that's the .env file). The lock (python-dotenv) knows how to use the key from your pocket.

### Why we used it

Our Groq API key gives access to the LLM. If we hardcoded it in the Python file and pushed to GitHub, anyone could steal it and use our quota.

### The code

```bash
# .env file (never commit this to GitHub)
GROQ_API_KEY=gsk_your_actual_key_here
```

```python
# In your Python file
from dotenv import load_dotenv
import os

load_dotenv()  # reads the .env file

api_key = os.getenv("GROQ_API_KEY")  # gets the value
```

### Key things to remember

- `.env` goes in `.gitignore` — never on GitHub
- `.env.example` goes on GitHub — shows what keys are needed but not their values
- `os.getenv("KEY")` returns `None` if the key doesn't exist — always test this

---

## 1.4 Classes and OOP (Object Oriented Programming)

### Plain English

A class is a template or blueprint. You define what something looks like once, then create as many copies (objects) as you want from that template.

### Analogy

A cookie cutter is a class. Each cookie you make from it is an object. The cutter defines the shape; the cookies are individual instances with their own toppings.

### Why we used it

We built a `DataPipeline` class to organise our data cleaning steps. LangChain, FastAPI, and Pydantic all use classes heavily — you need to read them.

### The code

```python
class DataPipeline:
    def __init__(self, raw_path, output_path):
        # __init__ runs when you create an object
        # self refers to this specific object
        self.raw_path = raw_path
        self.output_path = output_path
        self.data = None

    def load(self):
        print(f"Loading from {self.raw_path}")
        # ... load data ...
        return self  # returning self allows chaining

    def clean(self):
        print("Cleaning data...")
        # ... clean data ...
        return self

# Create an object from the class
pipeline = DataPipeline("data/raw/articles.json", "data/processed/clean.json")

# Use the object
pipeline.load().clean()  # chaining works because we return self
```

### Key things to remember

- `__init__` = the constructor — runs when object is created
- `self` = refers to the current object instance
- Classes organise related functions and data together
- You don't need to master OOP — just read and use classes

---

## 1.5 Exception Handling (try/except)

### Plain English

Exception handling lets your code deal with errors gracefully instead of crashing. You "try" something, and if it fails, you "except" the error and handle it.

### Analogy

You try to open a door. If it's locked (error), you don't panic and run away — you knock or find another door. try/except is the "don't panic" instruction.

### Why we used it

API calls fail. Files don't exist. Networks time out. Without try/except, one error crashes your entire pipeline. With it, you catch the error, log it, and continue.

### The code

```python
import requests

def fetch_article(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # raises error if status is 4xx or 5xx
        return response.json()
    except requests.exceptions.Timeout:
        print(f"Timed out: {url}")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
```

### Key things to remember

- Always use try/except around API calls, file operations, and database queries
- Catch specific exceptions first (Timeout, HTTPError), then general Exception last
- Return None or a default value on error — don't let the whole program crash
- Log the error message so you know what went wrong

---

## 1.6 File I/O and JSON

### Plain English

File I/O means reading from and writing to files. JSON is a text format for storing structured data (like a Python dictionary saved as text).

### Analogy

JSON is like a well-organised filing cabinet. Each drawer has a label (key) and contains documents (values). You can open the cabinet (read), add files (write), or update them.

### The code

```python
import json
from pathlib import Path

# Writing JSON
data = [{"id": 1, "text": "Article about diabetes..."}]

with open("data/processed/articles.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

# Reading JSON
with open("data/processed/articles.json", "r", encoding="utf-8") as f:
    loaded = json.load(f)

print(loaded[0]["text"])  # Article about diabetes...

# Creating directories if they don't exist
Path("data/processed").mkdir(parents=True, exist_ok=True)
```

### Key things to remember

- Always use `encoding="utf-8"` to handle special characters
- `json.dump()` writes Python object to file
- `json.load()` reads file back into Python object
- `Path.mkdir(parents=True, exist_ok=True)` creates all folders in the path

---

## 1.7 List Comprehensions

### Plain English

A list comprehension is a compact way to create a new list by transforming or filtering another list — all in one line.

### Analogy

Imagine you have a basket of apples. A list comprehension is like saying "give me all the red apples from the basket, polished" — in one instruction instead of a loop.

### The code

```python
articles = [
    {"text": "Diabetes study...", "word_count": 150},
    {"text": "Short.", "word_count": 5},
    {"text": "Insulin research...", "word_count": 200},
]

# Old way (for loop)
long_articles = []
for a in articles:
    if a["word_count"] >= 50:
        long_articles.append(a["text"])

# New way (list comprehension — same result)
long_articles = [a["text"] for a in articles if a["word_count"] >= 50]

# Read it right to left:
# "give me a['text']  for every a in articles  if a['word_count'] >= 50"
```

### Key things to remember

- Format: `[expression for item in list if condition]`
- The `if condition` part is optional
- Used constantly in data processing — learn to read them fluently

---

# PART 2 — DATA ENGINEERING

---

## 2.1 pandas DataFrames

### Plain English

pandas is Python's data manipulation library. A DataFrame is like an Excel spreadsheet in Python — rows and columns of data you can filter, sort, and transform.

### Analogy

If your data is a classroom of students, pandas is the teacher's gradebook. You can find all students who scored above 80, calculate the class average, or sort by name — all with one line of code.

### Why we used it

We used pandas to clean 200 raw PubMed articles — removing empty rows, stripping whitespace, filtering short articles, removing duplicates.

### The code

```python
import pandas as pd

# Load data
df = pd.DataFrame([
    {"pmid": "123", "text": "  Diabetes study...  ", "year": 2023},
    {"pmid": "124", "text": "", "year": None},
    {"pmid": "125", "text": "Insulin research...", "year": 2023},
])

print(df.shape)           # (3, 3) — 3 rows, 3 columns
print(df.isnull().sum())  # count missing values per column

# Cleaning
df = df.dropna(subset=["text"])        # remove rows where text is empty
df["text"] = df["text"].str.strip()    # remove whitespace
df["word_count"] = df["text"].apply(   # add new column
    lambda x: len(x.split())
)
df = df[df["word_count"] >= 10]        # filter short articles
df = df.drop_duplicates(subset=["text"])  # remove duplicates
df = df.reset_index(drop=True)         # reset row numbers

# Convert back to list of dictionaries
records = df.to_dict(orient="records")
```

### Key things to remember

- `df.shape` → (rows, columns)
- `df.isnull().sum()` → count missing values
- `df.dropna()` → remove rows with missing values
- `df.apply(func)` → apply a function to every row
- `df[condition]` → filter rows where condition is True
- `df.to_dict(orient="records")` → convert to list of dicts

---

## 2.2 REST APIs and the requests Library

### Plain English

A REST API is a way for programs to talk to each other over the internet using URLs. The `requests` library lets Python send those messages and receive responses.

### Analogy

A REST API is like a restaurant menu. You send an order (request) to the kitchen (server), and they send back your food (response). The menu tells you what you can order and in what format.

### Why we used it

We used the PubMed API to fetch 200 real medical research abstracts for free. No account needed — just send a GET request to their URL with your search query.

### The code

```python
import requests
import time

def fetch_pubmed_ids(query, max_results=200):
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "json"
    }
    response = requests.get(url, params=params, timeout=15)
    return response.json()["esearchresult"]["idlist"]

def fetch_abstract(pmid):
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {"db": "pubmed", "id": pmid, "retmode": "text", "rettype": "abstract"}
    try:
        r = requests.get(url, params=params, timeout=15)
        return {"pmid": pmid, "text": r.text.strip()}
    except Exception as e:
        print(f"Failed {pmid}: {e}")
        return None

# Usage
ids = fetch_pubmed_ids("diabetes treatment 2023", max_results=200)
for pmid in ids:
    article = fetch_abstract(pmid)
    time.sleep(0.4)  # be polite — don't hammer the API
```

### Key things to remember

- `requests.get(url, params=params)` sends a GET request
- `response.json()` parses the JSON response into a Python dict
- Always set `timeout` — without it your code can hang forever
- Always add `time.sleep()` between API calls to avoid being blocked
- HTTP 200 = success, 404 = not found, 429 = rate limited, 500 = server error

---

# PART 3 — AI/NLP CORE CONCEPTS

---

## 3.1 What are Embeddings?

### Plain English

Embeddings convert text into a list of numbers that capture meaning. Similar words/sentences get similar numbers. Different topics get different numbers.

### Analogy

Imagine a map where every word is a city. Cities (words) that are similar are placed close together on the map. "Cat" and "kitten" are neighbouring cities. "Car" and "kitten" are far apart. Embeddings are the GPS coordinates of each city.

### Why we used it

To search our 1,336 medical chunks by meaning — not just keywords. When you ask "blood sugar management", it finds chunks about "diabetes treatment" because they have similar embeddings.

### The code

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

sentences = [
    "Diabetes is treated with insulin",       # medical
    "Blood sugar management requires drugs",   # medical — similar
    "Football is a popular sport",             # unrelated
]

embeddings = model.encode(sentences)
# Each sentence → 384 numbers
# Sentence 1 and 2 will have similar numbers
# Sentence 3 will have very different numbers

print(f"Shape: {embeddings.shape}")  # (3, 384)
print(f"First 3 numbers of sentence 1: {embeddings[0][:3]}")
```

### Key things to remember

- `all-MiniLM-L6-v2` produces 384-dimensional vectors
- Runs completely free on your laptop — no API needed
- Similar meaning = vectors point in similar directions
- This is the foundation of semantic search

---

## 3.2 Cosine Similarity

### Plain English

Cosine similarity measures how similar two vectors (embeddings) are. Score of 1.0 = identical meaning. Score of 0.0 = completely different. Score between 0.6–0.7 = good match.

### Analogy

Imagine two people pointing in directions. If they both point North, they're pointing the same way (similarity = 1). If one points North and one points South, they're opposite (similarity = -1). Cosine similarity measures the angle between them — not distance, but direction.

### The code

```python
import numpy as np

def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    magnitude = np.linalg.norm(vec1) * np.linalg.norm(vec2)
    return dot_product / magnitude

# In your project — comparing all chunks to a query
query_embedding = model.encode(["What treats diabetes?"])[0]
chunk_embeddings = model.encode(["Insulin treats diabetes", "Football rules"])

for i, chunk_emb in enumerate(chunk_embeddings):
    sim = cosine_similarity(query_embedding, chunk_emb)
    print(f"Chunk {i}: similarity = {round(sim, 3)}")
# Chunk 0: similarity = 0.721  ← good match
# Chunk 1: similarity = 0.124  ← poor match
```

### Key things to remember

- Your evaluation showed avg similarity of 0.624 — that's good
- Above 0.6 = relevant match
- Below 0.4 = likely not relevant
- This is what powers your entire retrieval system

---

## 3.3 Chunking

### Plain English

Chunking splits long documents into smaller pieces so you can search them more precisely. Instead of searching a whole 500-word article, you search 100-word chunks and find exactly the right section.

### Analogy

If you want to find a recipe in a cookbook, you don't read the whole book — you look at chapter headings (chunks), then paragraphs. Chunking is like tearing the book into individual pages so you can find the exact right page.

### Why we used it

PubMed abstracts are 200–500 words. A query about "metformin dosage" shouldn't retrieve a whole abstract that mentions metformin once. It should retrieve the specific 100-word section about dosage.

### The code

```python
def chunk_text(text, chunk_size=100, overlap=20):
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = ' '.join(words[start:end])
        if len(chunk.strip()) > 30:  # skip tiny chunks
            chunks.append(chunk)
        start += (chunk_size - overlap)  # overlap prevents cutting sentences

    return chunks

# Example
text = "word " * 250  # 250 words
chunks = chunk_text(text, chunk_size=100, overlap=20)
print(f"250 words → {len(chunks)} chunks")  # about 3 chunks
```

### Key things to remember

- `chunk_size=100` = 100 words per chunk
- `overlap=20` = each chunk shares 20 words with the next (prevents cutting sentences in half)
- Each chunk gets its own embedding and is stored separately
- You created 1,336 chunks from 200 articles (avg ~6.7 chunks per article)

---

## 3.4 Vector Store (numpy implementation)

### Plain English

A vector store stores all your embeddings and lets you find the most similar ones to a query quickly. Your implementation uses numpy arrays saved to disk.

### Analogy

A vector store is a library where books are sorted by topic similarity, not alphabetically. Ask "books about diabetes" and it instantly finds the 5 most topically similar books — even if they don't use the word "diabetes".

### The code

```python
import numpy as np
from sentence_transformers import SentenceTransformer
from utils import load_json, save_json

STORE_PATH = 'data/vectorstore_simple'
EMBED_MODEL = 'all-MiniLM-L6-v2'

def build_simple_store():
    chunks = load_json('data/processed/chunks.json')
    embedder = SentenceTransformer(EMBED_MODEL)
    texts = [c['text'] for c in chunks]
    embeddings = embedder.encode(texts, show_progress_bar=True)
    np.save(f'{STORE_PATH}/embeddings.npy', embeddings)  # save to disk
    save_json(chunks, f'{STORE_PATH}/chunks.json')

def load_simple_store():
    embeddings = np.load(f'{STORE_PATH}/embeddings.npy')  # load from disk
    chunks = load_json(f'{STORE_PATH}/chunks.json')
    return embeddings, chunks

def simple_retrieve(query, n_results=5):
    embedder = SentenceTransformer(EMBED_MODEL)
    embeddings, chunks = load_simple_store()

    query_embedding = embedder.encode([query])[0]

    # Calculate similarity of query to ALL chunks at once
    similarities = np.dot(embeddings, query_embedding) / (
        np.linalg.norm(embeddings, axis=1) * np.linalg.norm(query_embedding)
    )

    # Get indices of top N most similar
    top_indices = np.argsort(similarities)[::-1][:n_results]

    return [{"text": chunks[i]['text'],
             "similarity": round(float(similarities[i]), 3)}
            for i in top_indices]
```

### Key things to remember

- `np.save()` and `np.load()` persist embeddings to disk
- `np.dot()` calculates dot products for all chunks simultaneously — very fast
- `np.argsort()[::-1]` sorts indices from highest to lowest similarity
- You replaced ChromaDB with this because Python 3.14 had compatibility issues

---

## 3.5 RAG — Retrieval Augmented Generation

### Plain English

RAG combines a search system (retrieval) with a language model (generation). Before the AI answers, it searches your documents for relevant context, then uses that context to generate a grounded answer.

### Analogy

Open-book exam. The question is asked (user query). You search your notes for relevant pages (retrieval). You read those pages and write your answer based on them (generation). You cite which pages you used (citations).

### The complete flow

```
User Question
     ↓
Convert to embedding (numbers)
     ↓
Search vector store for similar chunks
     ↓
Get top 5 most relevant chunks
     ↓
Build prompt: "Here are 5 research papers: [chunks]. Answer: [question]"
     ↓
Send prompt to Groq LLM
     ↓
LLM generates answer using ONLY the provided chunks
     ↓
Return answer + source citations
```

### The code

```python
def ask(question, n_chunks=5, chat_history=None):
    # Step 1: Retrieve relevant chunks
    chunks = retrieve(question, n_results=n_chunks)

    # Step 2: Build prompt with context
    system_prompt, user_message = build_prompt(question, chunks, chat_history)

    # Step 3: Send to Groq LLM
    response = client.chat.completions.create(
        model='llama-3.3-70b-versatile',
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_message}
        ],
        temperature=0.1,  # low = factual, high = creative
        max_tokens=500
    )

    return {
        'answer': response.choices[0].message.content,
        'sources': chunks,
        'latency': round(time.time() - start, 2),
        'tokens': response.usage.total_tokens
    }
```

### Key things to remember

- RAG prevents hallucination by grounding answers in real documents
- `temperature=0.1` = factual and consistent (good for medical info)
- `max_tokens=500` = limits answer length
- Your system achieved 100% citation rate — every answer traced to real papers
- The system prompt is WHERE you control hallucination — it says "only use provided sources"

---

## 3.6 Prompt Engineering

### Plain English

Prompt engineering is writing precise instructions to the LLM that make it behave exactly how you want. The system prompt sets the rules. The user message provides context and asks the question.

### Analogy

A system prompt is the job description you give a new employee on Day 1. "You are a medical research assistant. You only use provided sources. You always cite your sources. You never make things up." The employee (LLM) follows those rules for every task.

### The code

```python
def build_prompt(question, chunks, chat_history=None):
    # Format the retrieved chunks as context
    context_parts = []
    for i, chunk in enumerate(chunks):
        context_parts.append(
            f"[Source {i+1} | PMID: {chunk['pmid']}]\n{chunk['text']}"
        )
    context = "\n\n".join(context_parts)

    # System prompt — the rules
    system_prompt = """You are a medical research assistant.
You answer questions using ONLY the provided research abstracts.
Rules:
- Only use information from the provided sources
- Always cite: (Source 1), (Source 2) etc
- If sources don't contain the answer, say so honestly
- Never make up medical information"""

    # User message — context + question
    user_message = f"""Here are the relevant research abstracts:

{context}

Question: {question}

Answer using only the above sources and cite them."""

    return system_prompt, user_message
```

### Key things to remember

- System prompt = permanent instructions to the LLM
- User message = changes every query (context + question)
- "Only use provided sources" = the anti-hallucination rule
- Citation instructions = what makes answers trustworthy
- `temperature=0.1` + strict system prompt = factual, reliable answers

---

# PART 4 — BACKEND ENGINEERING

---

## 4.1 FastAPI

### Plain English

FastAPI is a Python framework for building web APIs. You write Python functions and add decorators (`@app.get`, `@app.post`) and FastAPI turns them into web endpoints that any application can call over the internet.

### Analogy

FastAPI is a waiter at a restaurant. It takes orders from customers (HTTP requests), goes to the kitchen (your Python functions), and brings back the food (responses). You just need to cook the food — FastAPI handles the waiter work.

### The code

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from rag_chain import ask

app = FastAPI(
    title="Healthcare RAG API",
    description="Ask medical questions answered from PubMed research",
    version="1.0.0"
)

# Define what the API accepts (input schema)
class QueryRequest(BaseModel):
    question: str
    n_chunks: Optional[int] = 5

# Define what the API returns (output schema)
class QueryResponse(BaseModel):
    answer: str
    sources: str
    latency: float
    tokens: int

# POST endpoint — accepts data, returns data
@app.post("/query", response_model=QueryResponse)
def query_rag(request: QueryRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    result = ask(request.question, n_chunks=request.n_chunks)
    return {
        "answer": result["answer"],
        "sources": result["sources_formatted"],
        "latency": result["latency"],
        "tokens": result["tokens"]
    }

# GET endpoint — just fetches data
@app.get("/health")
def health_check():
    return {"status": "healthy"}
```

### Running it

```bash
uvicorn api.main:app --host 127.0.0.1 --port 8000
# Then visit: http://127.0.0.1:8000/docs
```

### Key things to remember

- `@app.post("/query")` = create a POST endpoint at /query
- `@app.get("/health")` = create a GET endpoint at /health
- Pydantic models automatically validate input and output
- FastAPI auto-generates interactive docs at `/docs` — huge for interviews
- `HTTPException(status_code=400)` = bad input, user's fault
- `HTTPException(status_code=500)` = server error, your fault
- Uvicorn is the web server that runs FastAPI

---

## 4.2 Pydantic Models

### Plain English

Pydantic models define the shape of data your API accepts and returns. They automatically validate that data matches the expected format and types — rejecting invalid requests before they reach your code.

### Analogy

Pydantic is a bouncer at a club. Before anyone gets in (before data reaches your function), the bouncer checks: "Are you on the list? Do you have ID? Are you wearing the right shoes?" Invalid data gets rejected at the door with a clear error message.

### The code

```python
from pydantic import BaseModel
from typing import Optional

class QueryRequest(BaseModel):
    question: str           # required — must be a string
    n_chunks: Optional[int] = 5  # optional — defaults to 5 if not provided

# FastAPI automatically validates incoming requests against this model
# If someone sends {"question": 123} — it converts int to str
# If someone sends {} (no question) — it returns a 422 error automatically
```

### Key things to remember

- Inherits from `BaseModel`
- Fields with no default = required
- `Optional[type] = default` = optional field with default value
- Automatically rejects wrong data types
- Used in every professional Python API

---

## 4.3 HTTP Status Codes

### Plain English

HTTP status codes are numbers that tell you what happened with a request. Every web request you've ever made got one of these back.

### The important ones

| Code | Meaning               | When to use                |
| ---- | --------------------- | -------------------------- |
| 200  | OK — success          | Request worked fine        |
| 201  | Created               | New resource was created   |
| 400  | Bad Request           | User sent invalid data     |
| 401  | Unauthorized          | No/wrong API key           |
| 404  | Not Found             | URL doesn't exist          |
| 422  | Validation Error      | Pydantic rejected the data |
| 429  | Too Many Requests     | Rate limited               |
| 500  | Internal Server Error | Your code crashed          |

### Key things to remember

- 2xx = success
- 4xx = client error (user's fault)
- 5xx = server error (your fault)
- You saw 429 a LOT during this project — that's rate limiting

---

# PART 5 — FRONTEND AND UI

---

## 5.1 Streamlit

### Plain English

Streamlit converts Python scripts into web apps automatically. You write Python code using Streamlit functions and it renders buttons, text boxes, charts, and chat interfaces in a browser — no HTML or JavaScript needed.

### Analogy

Streamlit is like a magic translator. You speak Python, it speaks HTML/CSS/JavaScript. You say `st.button("Click me")` and Streamlit shows a button in the browser. You never have to learn web development.

### Key Streamlit functions we used

```python
import streamlit as st

# Page configuration
st.set_page_config(page_title="My App", layout="wide")

# Text elements
st.title("Big title")
st.caption("Small caption text")
st.markdown("**Bold** and *italic*")

# Layout
col1, col2 = st.columns([2, 1])  # 2:1 ratio split
with col1:
    st.write("Left column")
with col2:
    st.write("Right column")

# Chat interface
if question := st.chat_input("Ask a question..."):
    with st.chat_message("user"):
        st.write(question)
    with st.chat_message("assistant"):
        st.write("Answer here")

# Loading indicator
with st.spinner("Thinking..."):
    result = expensive_function()

# Collapsible section
with st.expander("Show sources"):
    st.write("Source details here")

# Metrics
st.metric("Response time", "2.3s")
```

### Key things to remember

- Streamlit re-runs the entire script every time user interacts
- That's why you need `st.session_state` to remember things
- Free deployment at share.streamlit.io
- `unsafe_allow_html=True` lets you inject custom CSS

---

## 5.2 st.session_state

### Plain English

`session_state` is Streamlit's memory. Because Streamlit re-runs your whole script on every interaction, normal Python variables get reset. `session_state` persists between re-runs.

### Analogy

Imagine a whiteboard that gets erased every time someone walks into the room. `session_state` is a notebook that you carry with you — it survives each room reset.

### The code

```python
import streamlit as st

# Initialize on first run
if "messages" not in st.session_state:
    st.session_state.messages = []

# Add to it (survives re-runs)
st.session_state.messages.append({
    "role": "user",
    "content": "What is metformin?"
})

# Read from it
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
```

### Key things to remember

- Always initialise with `if "key" not in st.session_state`
- Without it, chat history disappears every message
- `st.rerun()` forces a re-run while keeping session_state

---

# PART 6 — MLOPS AND ENGINEERING

---

## 6.1 pytest — Automated Testing

### Plain English

pytest is a library that runs test functions automatically. Each test asks a question about your code: "Does this function return what it should?" If yes — green tick. If no — red X with a clear explanation.

### Analogy

Tests are like a safety net under a tightrope walker. They don't stop you from walking — but if you fall (introduce a bug), they catch you immediately before the audience (users) notices.

### Why we used it

Every time you push code to GitHub, your tests run automatically (via GitHub Actions). If a bug is introduced, the test fails and you know immediately — before it reaches users.

### The code

```python
# tests/test_pipeline.py
import sys
sys.path.append('src')

def test_chunker_splits_text():
    from chunker import chunk_text
    text = "word " * 200  # 200 words
    chunks = chunk_text(text, chunk_size=100, overlap=20)
    assert len(chunks) > 1, "Long text should produce multiple chunks"

def test_utils_load_json_missing_file():
    from utils import load_json
    result = load_json("data/nonexistent_file.json")
    assert result is None, "Missing file should return None not crash"

def test_utils_clean_text():
    from utils import clean_text
    messy = "  hello    world  \n\n test  "
    result = clean_text(messy)
    assert result == "hello world test"
```

### Running tests

```bash
pytest tests/ -v
# -v means verbose — shows each test name and pass/fail
```

### Key things to remember

- Test functions must start with `test_`
- `assert condition, "message"` — if condition is False, test fails
- Write tests for: edge cases, missing files, invalid input
- Tests run automatically on GitHub Actions on every push
- Your project had 5 tests, all passing

---

## 6.2 Docker

### Plain English

Docker packages your entire application — Python, libraries, code, everything — into a container (a lightweight box) that runs identically on any computer. Solves "it works on my machine" forever.

### Analogy

A shipping container. Before containers, moving goods between ships was chaotic — different sizes, shapes, methods. Containers standardised everything. Same box, any ship, any port. Docker does the same for software.

### The Dockerfile we wrote

```dockerfile
FROM python:3.11-slim        # Start with Python 3.11 installed

WORKDIR /app                  # All our files go in /app

COPY requirements.txt .       # Copy requirements first (for caching)
RUN pip install --no-cache-dir -r requirements.txt  # Install libraries

COPY . .                      # Copy all project files

EXPOSE 8501                   # Open port 8501 for Streamlit

CMD ["streamlit", "run",      # When container starts, run chatbot
     "app/chatbot.py",
     "--server.port=8501",
     "--server.address=0.0.0.0"]
```

### Key commands

```bash
docker build -t healthcare-rag .    # Build the image
docker run -p 8501:8501 healthcare-rag  # Run it
docker run hello-world              # Test Docker works
```

### Key things to remember

- `FROM` = base image to start from
- `WORKDIR` = working directory inside the container
- `COPY` = copy files into the container
- `RUN` = execute a command during build
- `CMD` = what runs when container starts
- We couldn't run Docker locally due to Python 3.14 issues — but the Dockerfile is on GitHub

---

## 6.3 GitHub Actions — CI/CD

### Plain English

GitHub Actions is a robot that watches your repository. When you push code, it automatically runs your tests on GitHub's servers. CI (Continuous Integration) = auto-testing. CD (Continuous Deployment) = auto-deploying.

### Analogy

A factory quality inspector. Every time a new product comes off the line (code push), the inspector automatically checks it against quality standards (tests). Defective products (failing tests) are flagged before they reach customers (users).

### The YAML file we wrote

```yaml
# .github/workflows/ci.yml
name: CI Pipeline

on: # When to run
  push:
    branches: [main] # On every push to main

jobs:
  test:
    runs-on: ubuntu-latest # Use GitHub's Ubuntu server

    steps:
      - name: Checkout code
        uses: actions/checkout@v3 # Download your code

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.11" # Install Python

      - name: Install dependencies
        run: |
          pip install pytest sentence-transformers pandas requests python-dotenv

      - name: Run tests
        run: |
          pytest tests/ -v          # Run your tests
```

### Key things to remember

- YAML files use indentation for structure (like Python)
- `on: push: branches: [main]` = trigger on every push to main
- `runs-on: ubuntu-latest` = runs on GitHub's free Linux server
- Your CI is visible as a green ✅ or red ❌ on your GitHub repo
- Recruiters notice green CI badges — it signals professional engineering

---

# PART 7 — DEPLOYMENT

---

## 7.1 Streamlit Cloud Deployment

### Plain English

Streamlit Cloud reads your GitHub repository, installs your requirements.txt, and runs your app at a public URL — for free. Any change you push to GitHub automatically redeploys.

### How it works

```
You push code to GitHub
        ↓
Streamlit Cloud detects the change
        ↓
Pulls your latest code
        ↓
Installs requirements.txt
        ↓
Runs: streamlit run app/chatbot.py
        ↓
App available at your-app.streamlit.app
```

### Secrets management

```toml
# .streamlit/secrets.toml (never commit this)
GROQ_API_KEY = "gsk_your_key_here"
```

```python
# In your app — reads from Streamlit Cloud's secure vault
import streamlit as st
import os

if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
```

### Key things to remember

- Free hosting for public apps
- Secrets added in Streamlit Cloud dashboard — never in code
- `runtime.txt` can specify Python version (doesn't always work)
- Your app: healthcare-rag-29.streamlit.app

---

# PART 8 — YOUR PROJECT METRICS

---

## What you built — the numbers

| Metric                   | Value                           |
| ------------------------ | ------------------------------- |
| PubMed articles fetched  | 200                             |
| Chunks created           | 1,336                           |
| Avg words per chunk      | 100                             |
| Embedding dimensions     | 384                             |
| Embedding model          | all-MiniLM-L6-v2                |
| LLM model                | Groq LLaMA 3.3 70B              |
| Citation rate            | 100%                            |
| Avg retrieval similarity | 0.624                           |
| Avg query latency        | 8.43s                           |
| Pytest tests passing     | 5/5                             |
| GitHub CI status         | ✅ Green                        |
| Live URL                 | healthcare-rag-29.streamlit.app |

---

## Interview answers — memorise these

**"What is RAG?"**
RAG stands for Retrieval Augmented Generation. Before the AI answers, it searches a knowledge base for relevant context, then generates an answer using only that context. It's like an open-book exam — find the relevant pages, then write your answer based on them. This prevents hallucination because the AI is constrained to real, cited sources.

**"What are embeddings?"**
Embeddings convert text into numbers that capture semantic meaning. Similar sentences get similar numbers. We use them for semantic search — finding relevant documents by meaning rather than keyword matching. In my project I used sentence-transformers to generate 384-dimensional embeddings for 1,336 medical research chunks.

**"Why did you build a custom vector store instead of ChromaDB?"**
ChromaDB had compatibility issues with Python 3.14 on Streamlit Cloud. I replaced it with a pure numpy implementation using cosine similarity — same mathematical foundation, zero external dependencies, works on any Python version. This was actually a better engineering decision for deployment simplicity.

**"What is CI/CD?"**
CI/CD stands for Continuous Integration and Continuous Deployment. In my project I set up GitHub Actions to automatically run my 5 pytest tests every time I push code to GitHub. This catches bugs before they reach users and signals to recruiters that I think about code quality, not just features.

**"How did you evaluate your RAG system?"**
I built a custom evaluation script that ran 10 domain-specific medical questions through the system and measured: citation rate (100%), average retrieval similarity (0.624), average latency (8.43s), and average tokens per query (1,103). I documented these in docs/evaluation.md.

---

## Error reading guide

**Always read Python errors from the BOTTOM UP.**

The last line = the actual problem.
Everything above = how we got there.

| Error                       | Meaning                           | Fix                                       |
| --------------------------- | --------------------------------- | ----------------------------------------- |
| `ModuleNotFoundError`       | Library not installed             | `pip install library-name`                |
| `FileNotFoundError`         | File doesn't exist                | Check path, run from project root         |
| `KeyError`                  | Dictionary key doesn't exist      | Check spelling, check if key exists first |
| `AttributeError`            | Object doesn't have that property | Check object type, check spelling         |
| `ImportError`               | Import statement failed           | Check library installed, check file path  |
| `401 Unauthorized`          | Wrong API key                     | Check .env file, check key format         |
| `429 Too Many Requests`     | Rate limited                      | Add time.sleep(), check quota             |
| `500 Internal Server Error` | Your code crashed on server       | Check logs                                |

---

_These notes cover every concept used in the Healthcare RAG project — from environment setup to production deployment._
