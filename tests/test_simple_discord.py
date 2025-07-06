#!/usr/bin/env python3
"""
Simple Discord connection test using discord.py
"""

import os
import asyncio

# Try using discord.py if available
try:
    import discord

    TOKEN = "YOUR_DISCORD_BOT_TOKEN"  # Replace with your actual token
    CHANNEL_ID = 1350964414286921749
    USER_ID = 176716772664279040

    intents = discord.Intents.default()
    intents.message_content = True
    intents.guilds = True

    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f"Successfully connected as {client.user}")
        channel = client.get_channel(CHANNEL_ID)
        if channel:
            print(f"Found channel: {channel.name}")
            try:
                await channel.send(f"Bot connected! Testing message for <@{USER_ID}>")
                print("Test message sent!")
            except Exception as e:
                print(f"Error sending message: {e}")
        else:
            print(f"Could not find channel with ID {CHANNEL_ID}")
        await client.close()

    @client.event
    async def on_error(event, *args, **kwargs):
        print(f"Error in {event}: {args}")

    print("Starting Discord bot test...")
    client.run(TOKEN)

except ImportError:
    print("discord.py not installed. Testing with HTTP request instead...")
    import requests

    # Test with Discord API directly
    TOKEN = "YOUR_DISCORD_BOT_TOKEN"  # Replace with your actual token
    headers = {"Authorization": f"Bot {TOKEN}", "Content-Type": "application/json"}

    # Try to get bot info
    response = requests.get("https://discord.com/api/v10/users/@me", headers=headers)
    print(f"Bot info request status: {response.status_code}")
    if response.status_code == 200:
        print(f"Bot info: {response.json()}")
    else:
        print(f"Error: {response.text}")
