# Test Scripts

These test scripts help verify that your Discord bot is working correctly before deploying it as an MCP server.

## Setup

Before running any tests, create a `.env.test` file with your Discord credentials:

```bash
cat > .env.test << EOF
DISCORD_TOKEN=YOUR_DISCORD_BOT_TOKEN
DISCORD_CHANNEL_ID=YOUR_CHANNEL_ID
DISCORD_USER_ID=YOUR_USER_ID
EOF
```

**Important**: Replace the placeholder values with your actual Discord bot token and IDs.

## Available Tests

- `test_connection.sh` - Quick test to verify Discord connection
- `test_bot.sh` - Run the full bot with your credentials
- `test_final.py` - Comprehensive MCP functionality test
- `test_mcp_client.py` - Test MCP protocol communication
- `test_simple_discord.py` - Basic Discord API verification

## Running Tests

```bash
# Make scripts executable
chmod +x *.sh *.py

# Run basic connection test
./test_connection.sh

# Run full MCP test
python3 test_final.py
```

## Security Note

Never commit your actual Discord token to version control. The test scripts use placeholders that you must replace with your actual credentials.