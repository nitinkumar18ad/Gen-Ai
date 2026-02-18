from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

system_prompt = """

"""




response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role":"user","content":"What is the current weather of Banglore?"}
    ]
)

print(response.choices[0].message.content)
