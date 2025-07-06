#!/bin/bash

echo "Testing minimal Discord bot connection..."
echo ""

# Export environment variables
export DISCORD_TOKEN="YOUR_DISCORD_BOT_TOKEN"  # Replace with your actual token
export DISCORD_CHANNEL_ID="1350964414286921749"
export DISCORD_USER_ID="176716772664279040"

# Run with Rust backtrace enabled
export RUST_BACKTRACE=1

echo "Running bot with environment variables..."
echo "Token: ${DISCORD_TOKEN:0:20}..."
echo "Channel: $DISCORD_CHANNEL_ID"
echo "User: $DISCORD_USER_ID"
echo ""

# Create a simple stdin input to send initialization
(
  sleep 3
  echo '{"jsonrpc":"2.0","method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{}},"id":1}'
  sleep 2
  echo '{"jsonrpc":"2.0","method":"notifications/initialized","id":null}'
  sleep 10
) | cargo run 2>&1 | tee test_output.log