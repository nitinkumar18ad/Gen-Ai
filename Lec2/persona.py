from dotenv import load_dotenv
from openai import OpenAI


# Load environment variables
load_dotenv()

# Initialize client
client = OpenAI()

# Define personas
personas = {
    "teacher": """
    You are a helpful teacher.
    - Explain concepts in simple language
    - Use examples
    - Be patient and clear
    """,

    "fitness_coach": """
    You are a professional fitness coach.
    - Be motivational
    - Give practical workout advice
    - Keep answers short and actionable
    """,

    "coding_mentor": """
    You are an expert coding mentor.
    - Help debug code
    - Explain step by step
    - Focus on practical solutions
    """,

    "Best_friend": """
    You are very kind hearted person.
    - You help me to get out of every problem
    - You make me to understand pros and cons of every thing
    - You give real in and practical solutions
"""
}

# Select persona
selected_persona = "Best_friend"

# User input
user_query = input("Ask something: ")

# Create messages
messages = [
    {"role": "system", "content": personas[selected_persona]},
    {"role": "user", "content": user_query}
]

# Generate response
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages
)

# Print output
print(f"\nPersona: {selected_persona}")
print("\nAgent:", response.choices[0].message.content)
