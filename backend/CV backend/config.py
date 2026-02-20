"""
Configuration file for Cover Letter Generator Backend
"""
import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
API_HOST = os.environ.get("API_HOST", "0.0.0.0")
API_PORT = int(os.environ.get("API_PORT", 8000))
DEBUG = os.environ.get("DEBUG", "False").lower() == "true"

# LLM Configuration
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
LLM_MODEL = os.environ.get("LLM_MODEL", "gpt-3.5-turbo")
MAX_TOKENS = int(os.environ.get("MAX_TOKENS", 600))

# Embedding Configuration
EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
EMBEDDING_DIMENSION = 384

# RAG Configuration
TOP_K_CHUNKS = int(os.environ.get("TOP_K_CHUNKS", 5))
CHUNK_SIZE = int(os.environ.get("CHUNK_SIZE", 500))

# Data Paths
DATA_DIR = os.environ.get("DATA_DIR", "./")
FAISS_INDEX_PATH = os.path.join(DATA_DIR, "faiss_index")
METADATA_PATH = os.path.join(DATA_DIR, "metadata.pkl")

# Cover Letter Rules
MIN_WORD_COUNT = 200
MAX_WORD_COUNT = 450
