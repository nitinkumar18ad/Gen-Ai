import json
import requests
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

# ------------------ TOOL ------------------
def get_weather(city: str):
    print(f"🔧 Tool called: get_weather({city})")
    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)
    return "something went wrong"

available_tools = {
    "get_weather": {
        "fn": get_weather,
        "description": "Takes a city name as input and returns the current weather of the city"
    }
}

# ------------------ SYSTEM PROMPT ------------------
system_prompt = """
You are a helpful AI assistant.

Follow steps: plan -> action -> observe -> output

Rules:
- Return JSON only
- One step at a time
- Be precise

JSON format:
{
 "step": "plan/action/observe/output",
 "content": "text",
 "function": "function_name_if_action",
 "input": "input_for_function"
}

Available tools:
- get_weather(city)
"""

messages = [{"role": "system", "content": system_prompt}]

# ------------------ USER INPUT ------------------
user_query = input("> ")
messages.append({"role": "user", "content": user_query})

# ------------------ LOOP ------------------
while True:
    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=messages
    )

    # FIX 1: correct property name (message not messages)
    content = response.choices[0].message.content
    parsed_output = json.loads(content)

    messages.append({"role": "assistant", "content": content})

    step = parsed_output.get("step")

    # ------------------ PLAN ------------------
    if step == "plan":
        print(f"🧠: {parsed_output.get('content')}")
        continue

    # ------------------ ACTION ------------------
    if step == "action":
        tool_name = parsed_output.get("function")
        tool_input = parsed_output.get("input")

        if tool_name in available_tools:
            output = available_tools[tool_name]["fn"](tool_input)

            # send observation back
            observation = {
                "step": "observe",
                "output": output
            }
            messages.append({
                "role": "assistant",
                "content": json.dumps(observation)
            })
        else:
            print("❌ Unknown tool")
            break

        continue

    # ------------------ OUTPUT ------------------
    if step == "output":
        print(f"🤖: {parsed_output.get('content')}")
        break
