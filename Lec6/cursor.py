from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import PlainTextResponse
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()


app = FastAPI()

# Read API key from environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Request body structure
class Query(BaseModel):
    prompt: str


@app.post("/query", response_class=PlainTextResponse)
async def handle_query(query: Query):

    # Print user query in terminal
    print(f"User Query: {query.prompt}")

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0,   # cleaner and more deterministic output
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a coding assistant like Cursor. "
                        "Give clear, direct answers. Return only the useful output."
                    )
                },
                {
                    "role": "user",
                    "content": query.prompt
                }
            ]
        )

        # Extract only the assistant message
        output = response.choices[0].message.content

        # Clean output
        if output:
            output = output.strip()

        return output

    except Exception as e:
        print("Error:", e)
        return f"Error: {str(e)}"