import os
from dotenv import load_dotenv

from mem0 import Memory
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

QDRANT_HOST = "localhost"

NEO4J_URL = "bolt://localhost:7687"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "reform-william-center-vibrate-press-5829"


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


def split_preferences(message):
    """
    Break sentences like:
    'I like React, JavaScript and MongoDB'
    'I like Roti with Chutni'
    into separate statements.

    """
    message = message.replace(" and ", ",")
    items = [i.strip() for i in message.split(",") if i.strip()]

    # convert to individual facts
    facts = []
    for item in items:
        if not item.lower().startswith("i"):
            facts.append(f"I like {item}")
        else:
            facts.append(item)

    return facts


def store_memory(message):
    facts = split_preferences(message)

    for fact in facts:
        mem_client.add(
            [{"role": "user", "content": fact}],
            user_id="NKY"
        )


def chat(message):

    mem_result = mem_client.search(
        query=message,
        user_id="NKY"
    )

    print("\nMEMORY:")
    print(mem_result)
    print()

    messages = [
        {
            "role": "system",
            "content": f"User memories: {mem_result}"
        },
        {
            "role": "user",
            "content": message
        }
    ]

    result = openai_client.chat.completions.create(
        model="gpt-4.1",
        messages=messages
    )

    reply = result.choices[0].message.content

    # store memory AFTER response
    store_memory(message)

    return reply


while True:

    message = input(">> ")

    if message.lower() in ["exit", "quit"]:
        break

    response = chat(message)

    print("BOT:", response)