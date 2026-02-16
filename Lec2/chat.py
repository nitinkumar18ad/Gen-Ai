from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

result = client.chat.completions.create(

    model = "gpt-4",
    messages=[
        {"role": "user","content": "what is 2 + 2 * 0"} #Zero Shot Prompting
    ]
)

print(result.choice[0].message.content)