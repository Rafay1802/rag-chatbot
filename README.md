# 🤖 RAG Web Chatbot

A production-grade AI chatbot that lets you **chat with any website**. Paste a URL, and instantly ask questions about its content using Retrieval Augmented Generation (RAG).

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.54-red)
![LangChain](https://img.shields.io/badge/LangChain-latest-green)
![Pinecone](https://img.shields.io/badge/Pinecone-Vector%20DB-purple)
![Groq](https://img.shields.io/badge/Groq-LLaMA%203.3-orange)

---

## 🚀 Demo

1. Enter any URL (e.g. a Wikipedia article, a blog post, a documentation page)
2. Click **Load URL**
3. Ask questions about the content in natural language
4. Get accurate, context-aware answers powered by LLaMA 3.3

---

## 🧠 How It Works

This project implements a **RAG (Retrieval Augmented Generation)** pipeline:

```
URL → Scrape → Chunk → Embed → Store in Pinecone
                                      ↓
Question → Search Pinecone → Retrieve relevant chunks → LLM → Answer
```

1. **Scraping** — BeautifulSoup extracts clean text from any webpage
2. **Chunking** — LangChain splits text into 500-token overlapping chunks
3. **Embedding** — Pinecone's integrated `llama-text-embed-v2` model converts chunks to vectors
4. **Storage** — Vectors stored in Pinecone's cloud vector database
5. **Retrieval** — On each question, the top 5 most relevant chunks are retrieved
6. **Generation** — Groq's LLaMA 3.3-70b generates an answer using only the retrieved context

---

## 🛠 Tech Stack

| Tool | Purpose |
|------|---------|
| **Streamlit** | Frontend UI |
| **LangChain** | Orchestration & text splitting |
| **Pinecone** | Vector database + embeddings |
| **Groq + LLaMA 3.3** | LLM for answer generation |
| **BeautifulSoup** | Web scraping |
| **Python 3.11** | Core language |

---

## ⚙️ Setup & Installation

### 1. Clone the repo
```bash
git clone https://github.com/Rafay1802/rag-web-chatbot.git
cd rag-web-chatbot
```

### 2. Create a virtual environment
```bash
python3.11 -m venv venv
source venv/bin/activate  # Mac/Linux
```

### 3. Install dependencies
```bash
pip install streamlit langchain langchain-groq langchain-pinecone langchain-text-splitters pinecone beautifulsoup4 requests python-dotenv
```

### 4. Set up environment variables
Create a `.env` file in the root directory:
```
PINECONE_API_KEY=your_pinecone_api_key
GROQ_API_KEY=your_groq_api_key
PINECONE_INDEX_NAME=rag-chatbot
```

### 5. Set up Pinecone Index
- Go to [app.pinecone.io](https://app.pinecone.io)
- Create an index with the integrated `llama-text-embed-v2` model
- Set dimensions to `1024` and metric to `cosine`

### 6. Run the app
```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`

---

## 📁 Project Structure

```
rag-web-chatbot/
├── app.py              # Streamlit UI
├── rag/
│   ├── scraper.py      # URL scraping & text chunking
│   ├── embedder.py     # Store chunks in Pinecone
│   └── retriever.py    # Query Pinecone + generate answer
├── .env                # API keys (not committed)
├── .gitignore
└── README.md
```

---

## 🔑 Getting API Keys

- **Pinecone** (free) → [app.pinecone.io](https://app.pinecone.io)
- **Groq** (free) → [console.groq.com](https://console.groq.com)

---

## 💡 Use Cases

- Chat with documentation pages
- Summarize and Q&A on news articles
- Extract insights from research papers
- Query company websites or blogs

---

## 📄 License

MIT License — feel free to use and modify.
