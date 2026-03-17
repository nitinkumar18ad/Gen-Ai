"""
Weather Agent with Langfuse Tracing + OpenAI
-------------------------------------------
- Uses OpenAI for response generation
- Uses Langfuse for tracing/logging
"""

import os
from dotenv import load_dotenv
from openai import OpenAI
from langfuse import Langfuse

# ─────────────────────────────────────────────
# Load environment variables
# ─────────────────────────────────────────────
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY")
LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY")

# ─────────────────────────────────────────────
# Initialize OpenAI client
# ─────────────────────────────────────────────
client = OpenAI(api_key=OPENAI_API_KEY)

# ─────────────────────────────────────────────
# Initialize Langfuse
# ─────────────────────────────────────────────
langfuse = Langfuse(
    public_key=LANGFUSE_PUBLIC_KEY,
    secret_key=LANGFUSE_SECRET_KEY,
    host="https://cloud.langfuse.com"  # default cloud
)

# ─────────────────────────────────────────────
# Weather Agent Function
# ─────────────────────────────────────────────
def get_weather_response(user_query: str):
    """
    Generates a weather-related response using OpenAI
    and logs the interaction in Langfuse.
    """

    # Create a trace
    trace = langfuse.trace(
        name="weather-agent",
        input={"query": user_query}
    )

    try:
        # Call OpenAI
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful weather assistant."},
                {"role": "user", "content": user_query}
            ],
            temperature=0.7
        )

        answer = response.choices[0].message.content

        # Log output to Langfuse
        trace.update(
            output={"response": answer}
        )

        return answer

    except Exception as e:
        trace.update(
            output={"error": str(e)}
        )
        return f"Error: {str(e)}"


# ─────────────────────────────────────────────
# Main Execution
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("🌦️ Weather Agent (Langfuse + OpenAI)")
    print("Type 'exit' to quit\n")

    while True:
        user_input = input("Ask weather: ")

        if user_input.lower() == "exit":
            break

        result = get_weather_response(user_input)
        print("\n🤖:", result)
        print("-" * 50)