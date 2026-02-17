from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

system_prompt = """
You are an AI assistant who is expert in breaking down complex problems and resolving user queries.

For the given user input:
- Analyze the problem
- Think step by step
- Produce output
- Validate it
- Then give final result

You must follow this sequence:
analyze → think → output → validate → result

Respond strictly in this format:

{{step: "analyze", content: "..."}}
{{step: "think", content: "..."}}
{{step: "output", content: "..."}}
{{step: "validate", content: "..."}}
{{step: "result", content: "..."}}

Example:
Input: What is 2+2
Output:
{{step: "analyze", content: "User is asking a basic math addition"}}
{{step: "think", content: "Add 2 and 2"}}
{{step: "output", content: "4"}}
{{step: "validate", content: "4 is correct"}}
{{step: "result", content: "2+2 is 4"}}
"""

user_input = input("Ask something: ")

response = client.responses.create(
    model="gpt-4o",
    input=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}
    ]
)

print(response.output_text)
