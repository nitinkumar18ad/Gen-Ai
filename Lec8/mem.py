import os
from dotenv import load_dotenv

from mem0 import Memory
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ---------------------------
# DATABASE CONFIG
# ---------------------------

QDRANT_HOST = "localhost"

NEO4J_URL = "bolt://localhost:7687"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "reform-william-center-vibrate-press-5829"

# ---------------------------
# MEM0 CONFIG
# ---------------------------

config = {
    "version": "v1.1",
    "embedder": {
        "provider": "openai",
        "config": {
            "api_key": OPENAI_API_KEY,
            "model": "text-embedding-3-small",
        },
    },
    "llm": {
        "provider": "openai",
        "config": {
            "api_key": OPENAI_API_KEY,
            "model": "gpt-4.1",
        },
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": QDRANT_HOST,
            "port": 6333,
        },
    },
    "graph_store": {
        "provider": "neo4j",
        "config": {
            "url": NEO4J_URL,
            "username": NEO4J_USERNAME,
            "password": NEO4J_PASSWORD,
        },
    },
}

mem_client = Memory.from_config(config)
openai_client = OpenAI(api_key=OPENAI_API_KEY)

# ---------------------------
# SYSTEM PROMPT
# ---------------------------

SYSTEM_PROMPT = """
You are a helpful AI assistant.

Use the user's stored memories when relevant to answer questions.
Each memory has a similarity score. Higher score means more relevant.

Use those memories naturally in your response.
"""

# ---------------------------
# STORE MULTIPLE MEMORIES
# ---------------------------

def store_memory(message):

    message = message.replace(" and ", ",")
    items = [i.strip() for i in message.split(",") if i.strip()]

    for item in items:
        if not item.lower().startswith("i"):
            item = f"I like {item}"

        mem_client.add(
            [{"role": "user", "content": item}],
            user_id="NKY"
        )


# ---------------------------
# CHAT FUNCTION
# ---------------------------

def chat(message):

    # Retrieve relevant memories
    mem_result = mem_client.search(
        query=message,
        user_id="NKY"
    )

    # Build memory context with score
    memory_context = ""

    for mem in mem_result["results"]:
        memory_context += f"""
Memory: {mem['memory']}
Score: {mem['score']}
"""

    print("\nMEMORY RETRIEVED:")
    print(memory_context)

    # Messages sent to the LLM
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT + "\n\nUser Memories:\n" + memory_context
        },
        {
            "role": "user",
            "content": message
        }
    ]

    # Generate response
    result = openai_client.chat.completions.create(
        model="gpt-4.1",
        messages=messages
    )

    reply = result.choices[0].message.content

    # Store memory
    store_memory(message)

    return reply


# ---------------------------
# CHAT LOOP
# ---------------------------

while True:

    message = input(">> ")

    if message.lower() in ["exit", "quit"]:
        break

    response = chat(message)

    print("BOT:-", response)