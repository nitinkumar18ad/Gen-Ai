#!/usr/bin/env python3
"""
Enhanced MCP Math Server
Supports:
1. JSON input (for MCP client)
2. Natural language input (for CLI)
"""

import json
import sys
import re


class MathMCPServer:
    def __init__(self):
        # Toggle this:
        # True  -> clean output (CLI)
        # False -> JSON output (for MCP client)
        self.HUMAN_MODE = True

    # ---------------- MCP HANDLERS ---------------- #

    def handle_message(self, message: dict) -> dict:
        message_type = message.get("type")

        if message_type == "initialize":
            return self.handle_initialize()
        elif message_type == "tools/list":
            return self.handle_tools_list()
        elif message_type == "tools/call":
            return self.handle_tool_call(message)
        else:
            return self.error_response(f"Unknown message type: {message_type}")

    def handle_initialize(self):
        return {
            "type": "initialize",
            "protocolVersion": "2024-11-05",
            "serverInfo": {
                "name": "Math MCP Server",
                "version": "1.0.0",
            },
        }

    def handle_tools_list(self):
        return {
            "type": "tools/list",
            "tools": ["add", "multiply"],
        }

    def handle_tool_call(self, message):
        tool_name = message.get("name")
        args = message.get("arguments", {})

        try:
            if tool_name == "add":
                result = self.add(args.get("a"), args.get("b"))
            elif tool_name == "multiply":
                result = self.multiply(
                    args.get("a"), args.get("b"), args.get("c")
                )
            else:
                return self.error_response(f"Unknown tool: {tool_name}")

            return self.success(result)

        except Exception as e:
            return self.error_response(str(e))

    # ---------------- OPERATIONS ---------------- #

    def add(self, a, b):
        if a is None or b is None:
            raise ValueError("Both numbers are required")
        return a + b

    def multiply(self, a, b, c):
        if a is None or b is None or c is None:
            raise ValueError("Three numbers are required")
        return a * b * c

    # ---------------- RESPONSES ---------------- #

    def success(self, result):
        return {
            "type": "tools/call_result",
            "result": result,
            "isError": False,
        }

    def error_response(self, msg):
        return {
            "type": "error",
            "error": msg,
        }

    # ---------------- TEXT INPUT SUPPORT ---------------- #

    def handle_text_input(self, text: str):
        text = text.lower()

        try:
            # Extract numbers (supports negatives + decimals)
            nums = list(map(float, re.findall(r"-?\d+\.?\d*", text)))

            if "add" in text and len(nums) == 2:
                return self.success(nums[0] + nums[1])

            if "multiply" in text and len(nums) == 3:
                return self.success(nums[0] * nums[1] * nums[2])

            return self.error_response("Invalid text input")

        except Exception as e:
            return self.error_response(str(e))

    # ---------------- MAIN LOOP ---------------- #

    def run(self):
        while True:
            try:
                line = sys.stdin.readline()
                if not line:
                    break

                line = line.strip()

                # Try JSON first
                try:
                    message = json.loads(line)
                    response = self.handle_message(message)
                except json.JSONDecodeError:
                    # fallback to natural language
                    response = self.handle_text_input(line)

                # ✅ Output formatting
                if self.HUMAN_MODE:
                    if response.get("type") == "tools/call_result":
                        print(f"Result: {response.get('result')}")
                    elif response.get("type") == "error":
                        print(f"Error: {response.get('error')}")
                    else:
                        print(json.dumps(response))
                else:
                    print(json.dumps(response))

                sys.stdout.flush()

            except Exception as e:
                error = {
                    "type": "error",
                    "error": f"Server error: {str(e)}",
                }
                print(json.dumps(error))
                sys.stdout.flush()


if __name__ == "__main__":
    MathMCPServer().run()