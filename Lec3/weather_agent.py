import json
import requests
from dotenv import load_dotenv
from openai import OpenAI

# ------------------ INIT ------------------
load_dotenv()
client = OpenAI()

# ------------------ TOOL 1: WEATHER ------------------
def get_weather(city: str):
    print(f"🔧 Tool called: get_weather({city})")

    try:
        city = city.strip()

        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
        geo_res = requests.get(geo_url, timeout=10).json()

        if "results" not in geo_res:
            return f"Error: Could not find location for {city}"

        lat = geo_res["results"][0]["latitude"]
        lon = geo_res["results"][0]["longitude"]

        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        weather_res = requests.get(weather_url, timeout=10).json()

        temp = weather_res["current_weather"]["temperature"]

        return str(temp)  # return only number for easy conversion

    except Exception as e:
        return f"Error: {str(e)}"


# ------------------ TOOL 2: CONVERSION ------------------
def celsius_to_fahrenheit(temp: str):
    print(f"🔧 Tool called: celsius_to_fahrenheit({temp})")

    try:
        c = float(temp)
        f = (c * 9/5) + 32
        return f"{round(f, 2)}°F"
    except:
        return "Error: Invalid temperature"


# ------------------ AVAILABLE TOOLS ------------------
available_tools = {
    "get_weather": {
        "fn": get_weather,
        "description": "Returns temperature in Celsius"
    },
    "celsius_to_fahrenheit": {
        "fn": celsius_to_fahrenheit,
        "description": "Converts Celsius to Fahrenheit"
    }
}

# ------------------ SYSTEM PROMPT ------------------
system_prompt = """
You are a helpful AI assistant.

Follow steps: plan -> action -> observe -> output

Rules:
- Return JSON only
- One step at a time
- Always use tools if needed
- If user asks for Fahrenheit, convert Celsius using celsius_to_fahrenheit

JSON format:
{
 "step": "plan/action/observe/output",
 "content": "text",
 "function": "function_name_if_action",
 "input": "input_for_function"
}

Available tools:
- get_weather(city) → returns temperature in Celsius
- celsius_to_fahrenheit(temp) → converts to Fahrenheit

Example:
User: Temperature of Bangalore in Fahrenheit?

Output:
{"step":"plan","content":"User wants temperature in Fahrenheit"}
{"step":"action","function":"get_weather","input":"Bangalore"}
{"step":"observe","output":"30"}
{"step":"action","function":"celsius_to_fahrenheit","input":"30"}
{"step":"observe","output":"86°F"}
{"step":"output","content":"Temperature in Bangalore is 86°F"}
"""

# ------------------ MESSAGE MEMORY ------------------
messages = [
    {"role": "system", "content": system_prompt}
]

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

            observation = {
                "step": "observe",
                "output": output
            }

            messages.append({
                "role": "assistant",
                "content": json.dumps(observation)
            })
        else:
            print("❌ Unknown tool:", tool_name)
            break

        continue

    # ------------------ OUTPUT ------------------
    if step == "output":
        print(f"🤖: {parsed_output.get('content')}")
        break
