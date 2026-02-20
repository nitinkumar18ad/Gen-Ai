import json
import requests
from dotenv import load_dotenv
from openai import OpenAI
import os

# ------------------ INIT ------------------
load_dotenv()
client = OpenAI()

# ------------------ TOOL: SAFE COMMAND ------------------
def run_command(command):
    print(f"🔧 Tool called: run_command({command})")

    # block dangerous commands
    blocked = ["del", "rm", "shutdown", "format"]

    if any(b in command.lower() for b in blocked):
        return "Error: Unsafe command"

    result = os.system(command)

    if result == 0:
        return "Command executed successfully"
    else:
        return "Error executing command"


# ------------------ TOOL: CREATE FILE ------------------
def create_file(filename: str):
    print(f"🔧 Tool called: create_file({filename})")
    try:
        with open(filename, "w") as f:
            pass
        return f"{filename} created successfully"
    except Exception as e:
        return f"Error: {str(e)}"


# ------------------ TOOL: WEATHER ------------------
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

        return str(temp)

    except Exception as e:
        return f"Error: {str(e)}"


# ------------------ TOOL: CONVERSION ------------------
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
    },
    "run_command": {
        "fn": run_command,
        "description": "Executes safe system commands"
    },
    "create_file": {
        "fn": create_file,
        "description": "Creates a file in current directory"
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
- Do NOT use OS commands like touch for file creation
- Use create_file tool to create files
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
- run_command(command) → executes safe system commands
- create_file(filename) → creates a file

Example:
User: Temperature of Bangalore in Fahrenheit?

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

            print(f"🔍: {output}")   # show tool output

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