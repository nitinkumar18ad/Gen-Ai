#!/usr/bin/env python3
"""
Test client for the Math MCP Server.
This demonstrates how to interact with the MCP server.
"""

import json
import os
import subprocess
import sys


class MCPClient:
    def __init__(self, server_script: str):
        """Initialize client and start server process."""
        self.process = subprocess.Popen(
            [sys.executable, server_script],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )

    def send_message(self, message: dict) -> dict:
        """Send a message to server and return parsed response."""
        try:
            # Send request
            self.process.stdin.write(json.dumps(message) + "\n")
            self.process.stdin.flush()

            # Read response
            response_line = self.process.stdout.readline()

            # Debug: check server stderr
            err = self.process.stderr.readline()
            if err:
                print("[Server Error]:", err.strip())

            if response_line:
                try:
                    return json.loads(response_line)
                except json.JSONDecodeError:
                    return {
                        "type": "error",
                        "error": "Invalid JSON from server",
                    }

            return {
                "type": "error",
                "error": "No response from server",
            }

        except Exception as e:
            return {
                "type": "error",
                "error": f"Client error: {str(e)}",
            }

    def initialize(self) -> dict:
        """Initialize the server."""
        return self.send_message({"type": "initialize"})

    def list_tools(self) -> dict:
        """List available tools."""
        return self.send_message({"type": "tools/list"})

    def call_tool(self, tool_name: str, arguments: dict) -> dict:
        """Call a tool with arguments."""
        return self.send_message(
            {
                "type": "tools/call",
                "name": tool_name,
                "arguments": arguments,
            }
        )

    def close(self):
        """Close the server connection."""
        if self.process.stdin:
            self.process.stdin.close()
        self.process.wait()


def main():
    print("=" * 60)
    print("Math MCP Server - Test Client")
    print("=" * 60)

    # Server path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    server_path = os.path.join(current_dir, "mathserver.py")

    client = MCPClient(server_path)

    try:
        print("\n1. Initializing server...")
        init_response = client.initialize()
        if not init_response:
            raise RuntimeError("No response from server during initialize")

        print(f"   [OK] Server initialized")

        print("\n2. Listing available tools...")
        tools_response = client.list_tools()
        if not tools_response:
            raise RuntimeError("No response from server during tools/list")

        print("   Available tools:")
        for tool in tools_response.get("tools", []):
            print(f"   [OK] {tool}")

        print("\n3. Testing ADD function (5 + 3)...")
        add_response = client.call_tool("add", {"a": 5, "b": 3})
        result = add_response.get("result")
        print(f"   [OK] Result: {result}")
        assert result == 8, f"Expected 8, got {result}"

        print("\n4. Testing ADD function with floats (2.5 + 1.5)...")
        add_response = client.call_tool("add", {"a": 2.5, "b": 1.5})
        result = add_response.get("result")
        print(f"   [OK] Result: {result}")
        assert result == 4.0, f"Expected 4.0, got {result}"

        print("\n5. Testing MULTIPLY function (2 * 3 * 4)...")
        multiply_response = client.call_tool(
            "multiply", {"a": 2, "b": 3, "c": 4}
        )
        result = multiply_response.get("result")
        print(f"   [OK] Result: {result}")
        assert result == 24, f"Expected 24, got {result}"

        print("\n6. Testing MULTIPLY function with floats (1.5 * 2.0 * 3.0)...")
        multiply_response = client.call_tool(
            "multiply", {"a": 1.5, "b": 2.0, "c": 3.0}
        )
        result = multiply_response.get("result")
        print(f"   [OK] Result: {result}")
        assert result == 9.0, f"Expected 9.0, got {result}"

        print("\n7. Testing with negative numbers (ADD: -5 + 10)...")
        add_response = client.call_tool("add", {"a": -5, "b": 10})
        result = add_response.get("result")
        print(f"   [OK] Result: {result}")
        assert result == 5, f"Expected 5, got {result}"

        print("\n8. Testing error handling (invalid tool)...")
        error_response = client.call_tool("invalid_tool", {})
        if error_response.get("type") == "error":
            print(f"   [OK] Error caught: {error_response.get('error')}")

        print("\n" + "=" * 60)
        print("[OK] All tests passed successfully!")
        print("=" * 60)

    except AssertionError as e:
        print(f"\n[FAIL] Test failed: {e}")
    except Exception as e:
        print(f"\n[FAIL] Error: {e}")
    finally:
        client.close()


if __name__ == "__main__":
    main()