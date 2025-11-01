#🧠 PaperPal – RAG-Based GenAI Chatbot

PaperPal is an intelligent Retrieval-Augmented Generation (RAG) chatbot built with FastAPI, designed to answer user queries based on uploaded PDFs or custom document data. It combines document retrieval, vector embeddings, and LLM-powered reasoning to deliver fast, accurate, and context-aware responses.

🚀 Features

📄 PDF Upload Support – Upload multiple PDFs for knowledge ingestion

🔍 RAG Pipeline – Uses FAISS/Chroma vector stores for semantic search and retrieval

🧠 LLM Integration – Powered by Groq API / OpenAI / Ollama (local models) for response generation

⚙️ FastAPI Backend – High-performance, async backend for quick query handling

🧩 Modular Architecture – Separate modules for embeddings, retrieval, and query orchestration

🔒 Offline Capability – Supports local inference using Ollama TinyLLM for privacy

🌐 CORS Enabled – Seamless frontend integration (e.g., Streamlit or React client)
