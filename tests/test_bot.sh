#!/bin/bash

# Load environment variables
export DISCORD_TOKEN="YOUR_DISCORD_BOT_TOKEN"  # Replace with your actual token
export DISCORD_CHANNEL_ID="1350964414286921749"
export DISCORD_USER_ID="176716772664279040"

echo "Starting Human-in-the-Loop Discord bot..."
echo "Channel ID: $DISCORD_CHANNEL_ID"
echo "User ID: $DISCORD_USER_ID"
echo ""

# Run the bot
cargo run -- --discord-token "$DISCORD_TOKEN" --discord-channel-id "$DISCORD_CHANNEL_ID" --discord-user-id "$DISCORD_USER_ID"