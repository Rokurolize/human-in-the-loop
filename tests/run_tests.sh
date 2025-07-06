#!/bin/bash

echo "=== Human-in-the-Loop Discord Bot Test Suite ==="
echo ""

# Load credentials from .env.test
if [ -f .env.test ]; then
    export $(cat .env.test | grep -v '^#' | xargs)
    echo "✓ Loaded environment variables from .env.test"
else
    echo "✗ .env.test file not found!"
    exit 1
fi

echo ""
echo "Configuration:"
echo "  Token: ${DISCORD_TOKEN:0:30}..."
echo "  Channel ID: $DISCORD_CHANNEL_ID"
echo "  User ID: $DISCORD_USER_ID"
echo ""

# Test 1: Verify Discord API access
echo "Test 1: Verifying Discord API access..."
python3 -c "
import requests
headers = {'Authorization': 'Bot $DISCORD_TOKEN'}
r = requests.get('https://discord.com/api/v10/users/@me', headers=headers)
if r.status_code == 200:
    print('  ✓ Discord API access confirmed')
    print(f'  ✓ Bot name: {r.json()[\"username\"]}#{r.json()[\"discriminator\"]}')
else:
    print(f'  ✗ Discord API error: {r.status_code} - {r.text}')
    exit(1)
"

if [ $? -ne 0 ]; then
    echo "  ✗ Failed to verify Discord API access"
    exit 1
fi

echo ""
echo "Test 2: Starting MCP server test..."
echo "  This will attempt to connect the bot and test the ask_human tool."
echo "  Please monitor your Discord channel for messages."
echo ""

# Create a test client script inline
python3 << 'EOF'
import json
import subprocess
import time
import threading
import os

def read_output(proc, name):
    while True:
        line = proc.stdout.readline() if name == "stdout" else proc.stderr.readline()
        if not line:
            break
        print(f"[{name}] {line.strip()}")

# Start the MCP server
print("Starting MCP server...")
proc = subprocess.Popen(
    ["cargo", "run", "--quiet"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    env=os.environ.copy()
)

# Start output readers
threading.Thread(target=read_output, args=(proc, "stdout"), daemon=True).start()
threading.Thread(target=read_output, args=(proc, "stderr"), daemon=True).start()

time.sleep(3)

if proc.poll() is not None:
    print(f"Server exited early with code: {proc.poll()}")
    exit(1)

try:
    # Send initialize
    print("\nSending initialize request...")
    init_req = {
        "jsonrpc": "2.0",
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {}
        },
        "id": 1
    }
    proc.stdin.write(json.dumps(init_req) + '\n')
    proc.stdin.flush()
    time.sleep(2)
    
    # Send initialized notification
    print("Sending initialized notification...")
    init_notif = {
        "jsonrpc": "2.0",
        "method": "notifications/initialized"
    }
    proc.stdin.write(json.dumps(init_notif) + '\n')
    proc.stdin.flush()
    time.sleep(2)
    
    # List tools
    print("Listing tools...")
    list_req = {
        "jsonrpc": "2.0",
        "method": "tools/list",
        "params": {},
        "id": 2
    }
    proc.stdin.write(json.dumps(list_req) + '\n')
    proc.stdin.flush()
    time.sleep(2)
    
    # Call ask_human
    print("\nCalling ask_human tool...")
    print("CHECK YOUR DISCORD CHANNEL NOW!")
    ask_req = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": "ask_human",
            "arguments": {
                "question": "Bot test successful! Reply with anything to confirm you see this message."
            }
        },
        "id": 3
    }
    proc.stdin.write(json.dumps(ask_req) + '\n')
    proc.stdin.flush()
    
    print("\nWaiting 15 seconds for Discord interaction...")
    time.sleep(15)
    
except Exception as e:
    print(f"Error: {e}")
finally:
    print("\nStopping server...")
    proc.terminate()
    proc.wait()
    
print("\nTest completed!")
EOF

echo ""
echo "=== Test Suite Complete ==="