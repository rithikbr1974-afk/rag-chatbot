"""All settings in one place. Override any of them with an environment variable of the same name (or .env)."""
import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).parent
load_dotenv(ROOT / ".env")

# Keep downloaded embedding models inside the project (C: is nearly full).
os.environ.setdefault("HF_HOME", str(ROOT / "models"))


def _get(name, default):
    value = os.environ.get(name)
    return type(default)(value) if value is not None else default


DOCS_DIR = Path(_get("DOCS_DIR", str(ROOT / "docs")))
INDEX_DIR = Path(_get("INDEX_DIR", str(ROOT / "index")))

# Embeddings: bge-small is 384-dim, ~130 MB, fast on CPU, and strong on retrieval benchmarks for its size.
EMBED_MODEL = _get("EMBED_MODEL", "BAAI/bge-small-en-v1.5")
# bge models were trained with this prefix on queries (not on passages).
QUERY_PREFIX = _get("QUERY_PREFIX", "Represent this sentence for searching relevant passages: ")

# Chunking, in words (~1.3 tokens per English word).
CHUNK_WORDS = _get("CHUNK_WORDS", 180)
CHUNK_OVERLAP = _get("CHUNK_OVERLAP", 40)

# Retrieval
TOP_K = _get("TOP_K", 5)
FETCH_K = _get("FETCH_K", 20)        # candidates fetched before MMR re-ranking
MMR_LAMBDA = _get("MMR_LAMBDA", 0.7)  # 1.0 = pure relevance, lower = more diverse
MIN_SCORE = _get("MIN_SCORE", 0.35)  # cosine similarity below this counts as "not found"

# Claude
MODEL = _get("CLAUDE_MODEL", "claude-opus-5-5")
EFFORT = _get("CLAUDE_EFFORT", "low")  # low | medium | high; low is plenty for grounded Q&A
MAX_TOKENS = _get("MAX_TOKENS", 4000)
HISTORY_TURNS = _get("HISTORY_TURNS", 4)
