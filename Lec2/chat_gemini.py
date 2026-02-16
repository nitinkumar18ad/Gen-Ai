from google import genai
from google.genai import types

from google import genai

# Only run this block for Gemini Developer API
client = genai.Client(api_key='AIzaSyBmBpK1JWkXSddJFERspWyHCqxrSwZ1TTg')


for chunk in client.models.generate_content_stream(
    model='gemini-2.5-flash', contents='2*2+6=?'
):
    print(chunk.text, end='')