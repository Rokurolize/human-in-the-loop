# Human-in-the-Loop MCP Server

A Discord bot that enables AI assistants to ask questions to humans in real-time through the Model Context Protocol (MCP).

<img width="845" alt="Human-in-the-Loop Discord interaction" src="https://github.com/user-attachments/assets/dcdbb1a7-cb71-446e-b44d-bfe637059acb" />

## What This Does

This MCP server creates a bridge between AI assistants (like Claude) and humans via Discord. When an AI needs human input, it can ask questions directly in Discord and wait for responses.

**Example use cases:**
- AI needs project-specific information only you know
- Confirmation before executing sensitive operations  
- Gathering requirements or preferences during development
- Getting feedback on generated content
- Handling ambiguous instructions that need clarification

## Quick Start (5 minutes)

### Prerequisites
- Rust 1.70+ ([install here](https://rustup.rs/))
- Discord account
- A Discord server where you have admin permissions

### 1. Create Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" → Name it (e.g., "AI Assistant Helper")
3. Go to "Bot" section in left sidebar
4. Click "Reset Token" → Copy the token (you'll need this!)
5. Under "Privileged Gateway Intents", enable:
   - ✅ MESSAGE CONTENT INTENT (required!)
6. Under "Bot Permissions", select:
   - Send Messages
   - Create Public Threads  
   - Read Message History
   - View Channels

### 2. Add Bot to Your Server

1. Still in Discord Developer Portal, go to "OAuth2" → "URL Generator"
2. Select scopes: `bot`
3. Select same permissions as above
4. Copy the generated URL and open it in browser
5. Select your server and authorize

### 3. Get Required IDs

Enable Discord Developer Mode:
- Desktop: Settings → Advanced → Developer Mode → ON
- Mobile: Settings → Advanced → Developer Mode

Then:
- **Channel ID**: Right-click any text channel → "Copy Channel ID"
- **Your User ID**: Right-click your username → "Copy User ID"

### 4. Install and Test

```bash
# Clone and build
git clone https://github.com/KOBA789/human-in-the-loop.git
cd human-in-the-loop
cargo build --release

# Create test config
cat > .env.test << EOF
DISCORD_TOKEN=YOUR_BOT_TOKEN_HERE
DISCORD_CHANNEL_ID=YOUR_CHANNEL_ID_HERE  
DISCORD_USER_ID=YOUR_USER_ID_HERE
EOF

# Test the connection
export $(grep -v '^#' .env.test | xargs)
cargo run --bin human-in-the-loop
```

If successful, the bot should appear online in your Discord server.

## Configuration for AI Assistants

### Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json` (Mac) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "human-in-the-loop": {
      "command": "/path/to/human-in-the-loop",
      "args": [
        "--discord-channel-id", "YOUR_CHANNEL_ID",
        "--discord-user-id", "YOUR_USER_ID"
      ],
      "env": {
        "DISCORD_TOKEN": "YOUR_BOT_TOKEN"
      }
    }
  }
}
```

### Claude Code (claude.ai/code)

Add to MCP settings:

```json
{
  "mcpServers": {
    "human-in-the-loop": {
      "command": "human-in-the-loop",
      "args": [
        "--discord-channel-id", "YOUR_CHANNEL_ID",
        "--discord-user-id", "YOUR_USER_ID"
      ]
    }
  }
}
```

Then set environment variable before starting Claude:
```bash
export DISCORD_TOKEN="YOUR_BOT_TOKEN"
claude
```

## How It Works

1. **AI asks a question**: When the AI uses the `ask_human` tool, it sends a question
2. **Bot creates thread**: A new thread is created in your Discord channel (or reuses existing)
3. **You get notified**: Bot mentions you with the question
4. **You respond**: Type your answer in the thread
5. **AI receives answer**: Your response is sent back to the AI

### Example Interaction

```
You: "Create a README for my project"
AI: "I'll help create a README. Let me ask you some questions about your project."
[AI uses ask_human tool]

Discord:
Bot: @YourName What is the main purpose of your project?
You: It's a tool for managing Discord bots
[Bot returns this to AI]

AI: "Great! Let me ask about the key features..."
```

## Testing Your Setup

### 1. Basic Connection Test

```bash
# Create test script
cat > test_connection.py << 'EOF'
import requests
import os

token = os.environ.get('DISCORD_TOKEN')
headers = {'Authorization': f'Bot {token}'}
r = requests.get('https://discord.com/api/v10/users/@me', headers=headers)

if r.status_code == 200:
    print(f"✅ Bot connected: {r.json()['username']}#{r.json()['discriminator']}")
else:
    print(f"❌ Error: {r.text}")
EOF

python3 test_connection.py
```

### 2. Full MCP Test

```bash
# Download test script
curl -O https://raw.githubusercontent.com/KOBA789/human-in-the-loop/main/test_final.py
python3 test_final.py
```

This will:
- Initialize MCP connection
- List available tools
- Send a test question to Discord
- Wait for your response

## Troubleshooting

### Bot not appearing online
- Verify token is correct (no extra spaces)
- Check bot was added to server with correct permissions
- Ensure MESSAGE CONTENT INTENT is enabled

### "Cannot execute action on this channel type" error
- Make sure channel is a regular text channel (not forum/announcement)
- Bot needs "Create Public Threads" permission
- Try a different channel

### No response from bot
- Check bot has "View Channel" permission
- Verify channel ID is correct
- Ensure you're replying in the thread, not main channel

### "Connection closed" errors
- Token might be invalid or regenerated
- Check environment variables are set correctly
- Try running with `--discord-token` flag directly

## Command Line Options

```bash
human-in-the-loop [OPTIONS]

OPTIONS:
    --discord-token <TOKEN>          Discord bot token (or use DISCORD_TOKEN env)
    --discord-channel-id <ID>        Channel ID for creating threads
    --discord-user-id <ID>           User ID to mention in questions
    -h, --help                       Print help information
```

## Building from Source

```bash
# Clone repository
git clone https://github.com/KOBA789/human-in-the-loop.git
cd human-in-the-loop

# Build release version
cargo build --release

# Binary will be at: target/release/human-in-the-loop
```

## Security Notes

- Never commit your Discord token to version control
- Use environment variables or secure secret management
- Bot token gives full access to your bot - keep it safe
- Consider using separate Discord servers for testing

## Common Issues and Solutions

| Issue | Solution |
|-------|----------|
| Bot offline | Check token, ensure bot added to server |
| No threads created | Verify channel permissions, check channel type |
| Can't find channel | Enable Developer Mode, use right-click → Copy ID |
| MCP timeout | Ensure bot successfully connected to Discord first |
| Missing user mention | Verify user ID is correct |

## Contributing

Contributions welcome! Please ensure:
- Tests pass: `cargo test`
- Code is formatted: `cargo fmt`
- No clippy warnings: `cargo clippy`

## License

MIT License - see LICENSE file for details

## Future Plans

- Migration to native MCP Elicitation when standardized
- Support for multiple concurrent conversations
- Configurable timeout settings
- Web dashboard for monitoring