from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import PlainTextResponse
from openai import OpenAI
import os

app = FastAPI()

# Initialize OpenAI client (use environment variable for security)
client = OpenAI(api_key=os.getenv("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"))

# Request body structure
class Query(BaseModel):
    prompt: str


@app.post("/query", response_class=PlainTextResponse)
async def handle_query(query: Query):

    # Print user query in terminal
    print("User query:", query.prompt)

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a coding assistant like Cursor. Help write, fix and explain code."
                },
                {
                    "role": "user",
                    "content": query.prompt
                }
            ]
        )

        result = response.choices[0].message.content.strip()

        # Return clean output (not JSON)
        return result

    except Exception as e:
        return f"Error: {str(e)}"