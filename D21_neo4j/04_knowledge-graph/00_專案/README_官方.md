_以下為原文_


This project aims to demonstrate the potential use of Neo4j graph database as memory of Langchain agent, which contains

1. An implementation of entity graph similar to `NetworkxEntityGraph`, with Neo4j as storage
2. An implementation of `BaseChatMemory` which make use Neo4j knowledge graph, extending existing `ConversationKGMemory` which uses `NetworkxEntityGraph` (in memory entity graph implemented with NetworkX)

# Prerequisite

1. Docker + Docker Compose, or a Neo4j database instance
2. Python
3. (Optional) venv

# Setup

1. Start the Neo4j database container with docker-compose, or prepare a Neo4j database instance (e.g. Neo4j Desktop, cloud instance etc.).
2. Access your Neo4j database with browser with `http://localhost:7474/browser/` (assuming that Neo4j database is hosted locally) and follow instructions in web UI to reset password. (Hint: initial username and password are both `neo4j`)
3. Copy .env.example to .env and fill in the variables, namely Neo4j database connection config, and OpenAI API secret key.
4. Initiate virtual environment and install dependencies (or manage dependencies in other way)

```powershell
python -m venv ./venv
pip install -r ./requirement.txt
```

5. Make sure that environment variable for Neo4j connection is configured properly, and Neo4j database is started without error, run the script `{PROJECT_ROOT}/scripts/add_index_for_neo4j_db.py` to create index needed for performing full-text search in Neo4j knowledge graph

```powershell
# In project root
python ./scripts/add_index_for_neo4j_db.py
```

6. Run the app with `python ./src/main.py` in project root.

# Notes

1. As the graph is stored in Neo4j database, it is persisted even after the bot is shutted down
2. To see the most updated knowledge graph, run `MATCH (n) RETURN n` query in web UI of Neo4j to dump all nodes and edges. Beware that this query is slow if you have many nodes
