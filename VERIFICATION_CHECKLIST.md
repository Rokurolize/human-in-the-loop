# Human-in-the-Loop Discord Bot Verification Checklist

## Pre-deployment Testing

### 1. Environment Setup ✓
- [x] Discord bot token configured: `YOUR_DISCORD_BOT_TOKEN`
- [x] Discord channel ID configured: `1350964414286921749`
- [x] Discord user ID configured: `176716772664279040`
- [x] Bot added to Discord server with required permissions
- [x] Test configuration files created (`.env.test`, test scripts)

### 2. Build Verification ✓
- [x] Project builds successfully with `cargo build`
- [x] No compilation errors or warnings
- [x] All dependencies resolved

### 3. Discord Connection Test
Run: `./test_connection.sh`
- [ ] Bot connects to Discord successfully
- [ ] Bot appears online in Discord server
- [ ] No authentication errors in console
- [ ] Bot has access to specified channel

### 4. Basic Functionality Test
Run: `./test_bot.sh`
- [ ] Bot starts without errors
- [ ] MCP server initializes correctly
- [ ] Bot responds to gateway events
- [ ] Can create threads in specified channel

### 5. MCP Integration Test
Run: `python3 test_mcp_client.py`
- [ ] MCP server accepts connections
- [ ] `initialize` method responds correctly
- [ ] `tools/list` returns `ask_human` tool
- [ ] `ask_human` tool creates Discord message
- [ ] Bot mentions the correct user
- [ ] Bot waits for and receives user response
- [ ] Response is returned to MCP client

### 6. Error Handling
- [ ] Bot handles invalid Discord credentials gracefully
- [ ] Bot handles network disconnections
- [ ] Bot handles missing channel permissions
- [ ] MCP server handles malformed requests

### 7. Thread Management
- [ ] Bot creates new thread for first question
- [ ] Bot reuses existing thread for subsequent questions
- [ ] Thread title is set from first question (max 100 chars)
- [ ] Thread auto-archives after one day

### 8. Security Checks
- [ ] Token is not logged in plain text
- [ ] Sensitive data is not exposed in error messages
- [ ] Bot only responds to specified user ID
- [ ] No hardcoded credentials in source code

## Test Commands

1. **Basic connection test:**
   ```bash
   ./test_connection.sh
   ```

2. **Full bot test:**
   ```bash
   ./test_bot.sh
   ```

3. **MCP client test:**
   ```bash
   python3 test_mcp_client.py
   ```

4. **Manual MCP test (in another terminal):**
   ```bash
   # Terminal 1: Start the bot
   ./test_bot.sh
   
   # Terminal 2: Send MCP commands
   echo '{"jsonrpc":"2.0","method":"initialize","params":{"protocolVersion":"2024-11-05"},"id":1}' | nc localhost <port>
   ```

## Troubleshooting

### Bot doesn't connect to Discord
- Verify token is correct and not regenerated
- Check bot has been added to server
- Ensure MESSAGE CONTENT intent is enabled in Discord Developer Portal

### Bot can't send messages
- Verify bot has Send Messages permission in channel
- Check channel ID is correct
- Ensure bot has Create Public Threads permission

### MCP server doesn't respond
- Check if bot started successfully
- Verify no other process is using the same port
- Check firewall settings

### User doesn't receive mentions
- Verify user ID is correct
- Check user has access to the channel
- Ensure user hasn't disabled mentions

## Deployment Ready Checklist

- [ ] All tests pass successfully
- [ ] Bot responds within acceptable time (< 5 seconds)
- [ ] Error handling is robust
- [ ] Security checks pass
- [ ] Documentation is complete
- [ ] Environment variables are properly configured

## Notes

- Bot name: Algernon#1887
- Application ID: 763366800213016606
- Required Gateway Intents: GUILD_MESSAGES, MESSAGE_CONTENT
- Required Permissions: Send Messages, Create Public Threads, Read Message History