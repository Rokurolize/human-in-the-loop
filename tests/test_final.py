#!/usr/bin/env python3
"""
Final test script for Human-in-the-Loop MCP server
"""

import json
import subprocess
import time
import threading
import sys
import os


class MCPTester:
    def __init__(self):
        self.proc = None
        self.responses = []

    def read_output(self):
        """Read and print output from the MCP server"""
        for line in iter(self.proc.stdout.readline, ""):
            if line:
                try:
                    data = json.loads(line)
                    self.responses.append(data)
                    print(f"\n📥 Response: {json.dumps(data, indent=2)}")
                except:
                    print(f"📄 Output: {line.strip()}")

    def read_errors(self):
        """Read and print errors from the MCP server"""
        for line in iter(self.proc.stderr.readline, ""):
            if line:
                print(f"⚠️  Error: {line.strip()}")

    def send(self, data):
        """Send JSON-RPC message to the server"""
        msg = json.dumps(data)
        print(f"\n📤 Sending: {msg}")
        self.proc.stdin.write(msg + "\n")
        self.proc.stdin.flush()
        time.sleep(0.5)  # Give server time to process

    def run_test(self):
        # Load environment
        os.environ["DISCORD_TOKEN"] = (
            "YOUR_DISCORD_BOT_TOKEN"  # Replace with your actual token
        )
        os.environ["DISCORD_CHANNEL_ID"] = "1391244686810812426"
        os.environ["DISCORD_USER_ID"] = "176716772664279040"

        print("🚀 Starting Human-in-the-Loop MCP Server Test")
        print("=" * 50)

        # Start the server
        self.proc = subprocess.Popen(
            ["cargo", "run", "--bin", "human-in-the-loop"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=os.environ,
        )

        # Start reader threads
        threading.Thread(target=self.read_output, daemon=True).start()
        threading.Thread(target=self.read_errors, daemon=True).start()

        # Give server time to start and connect to Discord
        print("\n⏳ Waiting for server to start and connect to Discord...")
        time.sleep(3)

        # Step 1: Initialize
        print("\n1️⃣  Step 1: Initialize MCP connection")
        self.send(
            {
                "jsonrpc": "2.0",
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "clientInfo": {"name": "test-client", "version": "1.0"},
                },
                "id": 1,
            }
        )
        time.sleep(1)

        # Step 2: Send initialized notification
        print("\n2️⃣  Step 2: Send initialized notification")
        self.send({"jsonrpc": "2.0", "method": "notifications/initialized"})
        time.sleep(1)

        # Step 3: List available tools
        print("\n3️⃣  Step 3: List available tools")
        self.send({"jsonrpc": "2.0", "method": "tools/list", "params": {}, "id": 2})
        time.sleep(2)

        # Step 4: Call ask_human tool
        print("\n4️⃣  Step 4: Test ask_human tool")
        print("🔔 CHECK YOUR DISCORD CHANNEL NOW!")
        print(f"   Channel ID: {os.environ['DISCORD_CHANNEL_ID']}")
        print(f"   The bot will mention user ID: {os.environ['DISCORD_USER_ID']}")

        self.send(
            {
                "jsonrpc": "2.0",
                "method": "tools/call",
                "params": {
                    "name": "ask_human",
                    "arguments": {
                        "question": "🎉 MCP Test Successful! Please reply with 'confirmed' to complete the test."
                    },
                },
                "id": 3,
            }
        )

        # Wait for Discord response
        print("\n⏳ Waiting 20 seconds for Discord response...")
        print("   Please reply to the bot message in Discord!")

        for i in range(20):
            time.sleep(1)
            print(f"   {20 - i} seconds remaining...", end="\r")

        print("\n")

        # Summary
        print("\n📊 Test Summary")
        print("=" * 50)
        print(f"Total responses received: {len(self.responses)}")

        # Clean up
        print("\n🛑 Stopping server...")
        self.proc.terminate()
        self.proc.wait()

        print("\n✅ Test completed!")


if __name__ == "__main__":
    tester = MCPTester()
    try:
        tester.run_test()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        if tester.proc:
            tester.proc.terminate()
