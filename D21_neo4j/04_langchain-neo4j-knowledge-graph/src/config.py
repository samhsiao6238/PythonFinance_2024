import os
from dotenv import load_dotenv

# Load env var from .env
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CHATGPT_MODEL = os.getenv("CHATGPT_MODEL")

# Neo4j database connection config
NEO4J_DB_URI = os.getenv("NEO4J_DB_URI")
NEO4J_DB_NAME = os.getenv("NEO4J_DB_NAME")
NEO4J_DB_USER = os.getenv("NEO4J_DB_USER")
NEO4J_DB_PASS = os.getenv("NEO4J_DB_PASS")
NEO4J_ENTITY_NAME_FULLTEXT_INDEX_NAME = os.getenv(
    "NEO4J_ENTITY_NAME_FULLTEXT_INDEX_NAME"
)
