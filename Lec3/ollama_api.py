from fastapi import FastAPI
from pydantic import BaseModel
from ollama import Client
from fastapi import Body

app = FastAPI()

# Connect to Ollama
client = Client(host="http://localhost:11434")

# Request model
class ChatRequest(BaseModel):
    prompt: str

# API route
@app.post("/chat")
def chat(message: str = Body(..., description="Chat message")):
    response = client.chat(
        model="gemma3:1b",
        messages=[   # ✅ FIXED HERE
            {"role": "user", "content": message}
        ]
    )

    return {
        "response": response["message"]["content"]
    }