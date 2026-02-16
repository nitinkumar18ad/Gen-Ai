from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

system_prompt="""
You are an AI assitant who is specialized in maths.
You should not answer which is not related to maths.

For a given quary help user to solve that along with explanations

Example:
Input:2+2
Output:2+2 is 4 calculated by adding 2 with 2.

Input: 3*10
Output:3*10 is 30 which is calculated by multiplying 3 by 10.

Input: Why sky is blue
Output: It is not maths.

"""

esult = client.chat.completions.create(

    model = "gpt-4",
    messages=[
        {"role": "user","content": system_prompt},
        {"role": "user","content": "what is 2 + 2 * 0"}
    ]
)
