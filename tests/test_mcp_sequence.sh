#!/bin/bash

export $(grep -v '^#' .env.test | xargs)

echo "Testing MCP initialization sequence..."

# Create a named pipe for bidirectional communication
mkfifo mcp_input 2>/dev/null || true
mkfifo mcp_output 2>/dev/null || true

# Start the MCP server in background
cargo run --bin human-in-the-loop < mcp_input > mcp_output 2>&1 &
MCP_PID=$!

# Give it time to start
sleep 2

# Function to send JSON-RPC message
send_message() {
    echo "$1" > mcp_input
    echo "Sent: $1"
}

# Read output in background
cat mcp_output &
CAT_PID=$!

# Send initialize request
send_message '{"jsonrpc":"2.0","method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{}},"id":1}'
sleep 1

# Send initialized notification (no id for notifications)
send_message '{"jsonrpc":"2.0","method":"notifications/initialized"}'
sleep 1

# List tools
send_message '{"jsonrpc":"2.0","method":"tools/list","params":{},"id":2}'
sleep 2

# Clean up
kill $MCP_PID $CAT_PID 2>/dev/null
rm -f mcp_input mcp_output