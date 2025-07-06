#!/usr/bin/env python3
"""
Proper MCP client implementation following the protocol spec
"""

import json
import subprocess
import time
import sys
from threading import Thread, Event
import os


class MCPClient:
    def __init__(self):
        self.proc = None
        self.response_event = Event()
        self.last_response = None

    def read_responses(self):
        """Read responses from the MCP server"""
        while self.proc and self.proc.poll() is None:
            try:
                line = self.proc.stdout.readline()
                if not line:
                    break
                response = json.loads(line)
                print(f"Response: {json.dumps(response, indent=2)}")
                self.last_response = response
                self.response_event.set()
            except json.JSONDecodeError as e:
                print(f"Failed to decode: {line.strip()}")
            except Exception as e:
                print(f"Error reading response: {e}")

    def read_errors(self):
        """Read stderr from the MCP server"""
        while self.proc and self.proc.poll() is None:
            line = self.proc.stderr.readline()
            if not line:
                break
            print(f"[STDERR] {line.strip()}")

    def send_request(self, method, params=None, id=1):
        """Send a JSON-RPC request and wait for response"""
        request = {"jsonrpc": "2.0", "method": method, "id": id}
        if params is not None:
            request["params"] = params

        message = json.dumps(request)
        print(f"\nSending: {message}")

        self.response_event.clear()
        self.proc.stdin.write(message + "\n")
        self.proc.stdin.flush()

        # Wait for response
        if self.response_event.wait(timeout=10):
            return self.last_response
        else:
            print("Timeout waiting for response")
            return None

    def start(self):
        """Start the MCP server"""
        env = os.environ.copy()
        env["DISCORD_TOKEN"] = (
            "YOUR_DISCORD_BOT_TOKEN"  # Replace with your actual token
        )
        env["DISCORD_CHANNEL_ID"] = "1350964414286921749"
        env["DISCORD_USER_ID"] = "176716772664279040"

        print("Starting MCP server...")
        self.proc = subprocess.Popen(
            [
                "cargo",
                "run",
                "--",
                "--discord-token",
                env["DISCORD_TOKEN"],
                "--discord-channel-id",
                env["DISCORD_CHANNEL_ID"],
                "--discord-user-id",
                env["DISCORD_USER_ID"],
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=0,  # Unbuffered
            env=env,
        )

        # Start reader threads
        Thread(target=self.read_responses, daemon=True).start()
        Thread(target=self.read_errors, daemon=True).start()

        # Give server time to start
        time.sleep(3)

        if self.proc.poll() is not None:
            print(f"Server exited with code: {self.proc.poll()}")
            return False

        return True

    def stop(self):
        """Stop the MCP server"""
        if self.proc:
            self.proc.terminate()
            self.proc.wait()


def main():
    client = MCPClient()

    if not client.start():
        print("Failed to start MCP server")
        return

    try:
        # Step 1: Initialize
        print("\n=== Step 1: Initialize ===")
        response = client.send_request(
            "initialize",
            {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "clientInfo": {"name": "test-client", "version": "1.0"},
            },
        )

        if not response or "error" in response:
            print("Failed to initialize")
            return

        # Step 2: Send initialized notification
        print("\n=== Step 2: Initialized notification ===")
        client.send_request("notifications/initialized", None, id=None)
        time.sleep(1)

        # Step 3: List tools
        print("\n=== Step 3: List tools ===")
        response = client.send_request("tools/list", {})

        # Step 4: Call ask_human tool
        print("\n=== Step 4: Call ask_human tool ===")
        print("NOTE: Check Discord for the bot message!")
        response = client.send_request(
            "tools/call",
            {
                "name": "ask_human",
                "arguments": {
                    "question": "Testing MCP server! Please reply 'It works!' to confirm the bot is functioning."
                },
            },
        )

        print("\nWaiting 20 seconds for Discord response...")
        time.sleep(20)

    finally:
        client.stop()


if __name__ == "__main__":
    main()
