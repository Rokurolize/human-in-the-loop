#!/bin/bash

# Load environment variables
export DISCORD_TOKEN="YOUR_DISCORD_BOT_TOKEN"  # Replace with your actual token
export DISCORD_CHANNEL_ID="1350964414286921749"
export DISCORD_USER_ID="176716772664279040"

echo "Testing Discord bot connection..."
echo "Starting bot with:"
echo "  Channel ID: $DISCORD_CHANNEL_ID"
echo "  User ID: $DISCORD_USER_ID"
echo ""
echo "The bot will start as an MCP server. To test:"
echo "1. Check if 'Algernon' bot appears online in your Discord server"
echo "2. The bot will wait for MCP client connections"
echo ""
echo "Press Ctrl+C to stop the bot"
echo ""

# Run the bot with a timeout for testing
timeout 30s cargo run -- \
    --discord-token "$DISCORD_TOKEN" \
    --discord-channel-id "$DISCORD_CHANNEL_ID" \
    --discord-user-id "$DISCORD_USER_ID"