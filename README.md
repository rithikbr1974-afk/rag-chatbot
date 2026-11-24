# rag-chatbot

A small retrieval-augmented chatbot: it indexes your own documents and answers questions from them.

- `config.py`: all settings, each one overridable by an environment variable or a `.env` file
  (`DOCS_DIR`, `INDEX_DIR`, `EMBED_MODEL`, ...). Embeddings default to `BAAI/bge-small-en-v1.5`, which runs on a CPU.
- `loaders.py`: reads documents into text chunks.

Status: early work in progress (settings and loaders only so far).
