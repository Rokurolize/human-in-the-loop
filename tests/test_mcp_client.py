#!/usr/bin/env python3
"""
Simple MCP client to test the human-in-the-loop server
"""

import json
import subprocess
import time
import sys
from threading import Thread
import os


def send_jsonrpc(proc, method, params=None, id=1):
    """Send a JSON-RPC request to the MCP server"""
    request = {"jsonrpc": "2.0", "method": method, "id": id}
    if params:
        request["params"] = params

    message = json.dumps(request)
    print(f"Sending: {message}")
    proc.stdin.write(message + "\n")
    proc.stdin.flush()


def read_response(proc):
    """Read responses from the MCP server"""
    while True:
        line = proc.stdout.readline()
        if not line:
            break
        try:
            response = json.loads(line)
            print(f"Received: {json.dumps(response, indent=2)}")
        except json.JSONDecodeError:
            print(f"Raw output: {line.strip()}")


def main():
    # Set environment variables
    os.environ["DISCORD_TOKEN"] = (
        "YOUR_DISCORD_BOT_TOKEN"  # Replace with your actual token
    )
    os.environ["DISCORD_CHANNEL_ID"] = "1350964414286921749"
    os.environ["DISCORD_USER_ID"] = "176716772664279040"

    print("Starting MCP server...")

    # Start the MCP server
    proc = subprocess.Popen(
        [
            "cargo",
            "run",
            "--",
            "--discord-token",
            os.environ["DISCORD_TOKEN"],
            "--discord-channel-id",
            os.environ["DISCORD_CHANNEL_ID"],
            "--discord-user-id",
            os.environ["DISCORD_USER_ID"],
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
    )

    # Start reader thread
    reader_thread = Thread(target=read_response, args=(proc,))
    reader_thread.daemon = True
    reader_thread.start()

    # Give the server time to start
    time.sleep(5)

    print("\n=== Testing MCP Server ===\n")

    # Test 1: Initialize
    print("1. Sending initialize request...")
    send_jsonrpc(
        proc, "initialize", {"protocolVersion": "2024-11-05", "capabilities": {}}, id=1
    )
    time.sleep(2)

    # Test 2: List tools
    print("\n2. Listing available tools...")
    send_jsonrpc(proc, "tools/list", {}, id=2)
    time.sleep(2)

    # Test 3: Call ask_human tool
    print("\n3. Testing ask_human tool...")
    print("Check your Discord channel for the question!")
    send_jsonrpc(
        proc,
        "tools/call",
        {
            "name": "ask_human",
            "arguments": {
                "question": "This is a test question from the MCP client. Please reply with 'Test successful!' to confirm the bot is working."
            },
        },
        id=3,
    )

    print("\nWaiting for response from Discord (30 seconds)...")
    time.sleep(30)

    # Cleanup
    proc.terminate()
    proc.wait()


if __name__ == "__main__":
    main()
