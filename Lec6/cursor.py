from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai

app = FastAPI()

# Add your Gemini API key
genai.configure(api_key="YOUR_GEMINI_API_KEY")

# Load Gemini model
model = genai.GenerativeModel("gemini-1.5-pro")

# Request format
class Query(BaseModel):
    prompt: str


@app.post("/generate")
async def generate_code(query: Query):

    system_prompt = f"""
You are an AI coding assistant like Cursor.

Rules:
1. First give the code.
2. Use clean code blocks.
3. Then give a short explanation.
4. Format output clearly.

User request:
{query.prompt}
"""

    response = model.generate_content(system_prompt)

    return {
        "response": response.text
    }