from mem0 import Memory

OPENAI_API_KEY = "OPENAI_API_KEY"

QUADRANT_HOST = "localhost"

NEO4J_URL="bolt://localhost:7687"
NEO4J_USERNAME="neo4j"
NEO4J_PASSWORD="sX6GVjl5PWeTV4QeLhftqcHSi7tO27ZMroNrD-dAd_w"

config = {
    "version": "v1.1",
    "embedder":{
        "provider":"openai",
        "config":{"api_key":OPENAI_API_KEY,"model":"text-embeddings-3-small"},

    },
    "llm":{"provider":"openai","config":{"api_key":OPENAI_API_KEY,"model":"gpt-4.1"}},
    "vector_store":{
        "provider":"qdrant",
        "config":{
            "host": QUADRANT_HOST,
            "port": 6333,
        },
    },
    "graph_store":{
        "provider":"neo4j",
        "config":{"url":NEO4J_URL,"username":NEO4J_USERNAME,"password":NEO4J_PASSWORD},
    },
}

# mem_client = Memory.from_config(config)