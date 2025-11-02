import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
VECTOR_STORE_PATH = "vector_store"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
MODEL_NAME = "gemini-2.5-flash"
EMBEDDING_MODEL = "text-embedding-004"
TEMPERATURE = 0.3
MAX_OUTPUT_TOKENS = 2048
