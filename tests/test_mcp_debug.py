#!/usr/bin/env python3
"""
Debug version of MCP client to see what's happening
"""

import json
import subprocess
import time
import sys
from threading import Thread
import os


def read_stderr(proc):
    """Read stderr from the MCP server"""
    while True:
        line = proc.stderr.readline()
        if not line:
            break
        print(f"STDERR: {line.strip()}")


def read_stdout(proc):
    """Read stdout from the MCP server"""
    while True:
        line = proc.stdout.readline()
        if not line:
            break
        print(f"STDOUT: {line.strip()}")


def main():
    # Set environment variables
    os.environ["DISCORD_TOKEN"] = (
        "YOUR_DISCORD_BOT_TOKEN"  # Replace with your actual token
    )
    os.environ["DISCORD_CHANNEL_ID"] = "1350964414286921749"
    os.environ["DISCORD_USER_ID"] = "176716772664279040"

    print("Starting MCP server with debug output...")

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
        env=os.environ.copy(),
    )

    # Start reader threads
    stderr_thread = Thread(target=read_stderr, args=(proc,))
    stderr_thread.daemon = True
    stderr_thread.start()

    stdout_thread = Thread(target=read_stdout, args=(proc,))
    stdout_thread.daemon = True
    stdout_thread.start()

    # Give the server time to start
    time.sleep(5)

    print("\n=== Sending Initialize ===")
    request = {
        "jsonrpc": "2.0",
        "method": "initialize",
        "params": {"protocolVersion": "2024-11-05", "capabilities": {}},
        "id": 1,
    }

    message = json.dumps(request)
    print(f"Sending: {message}")
    try:
        proc.stdin.write(message + "\n")
        proc.stdin.flush()
    except Exception as e:
        print(f"Error sending: {e}")

    # Wait for response
    time.sleep(5)

    # Check if process is still running
    if proc.poll() is not None:
        print(f"\nProcess exited with code: {proc.poll()}")
    else:
        print("\nProcess is still running")

    # Cleanup
    proc.terminate()
    proc.wait()


if __name__ == "__main__":
    main()
