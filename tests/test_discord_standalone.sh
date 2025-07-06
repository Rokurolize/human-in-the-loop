#!/bin/bash

# Load environment variables
export DISCORD_TOKEN="YOUR_DISCORD_BOT_TOKEN"  # Replace with your actual token
export DISCORD_CHANNEL_ID="1350964414286921749"
export DISCORD_USER_ID="176716772664279040"

echo "Compiling Discord standalone test..."
rustc --edition 2021 test_discord_only.rs \
    --extern serenity=target/debug/deps/libserenity-*.rlib \
    --extern tokio=target/debug/deps/libtokio-*.rlib \
    --extern async_trait=target/debug/deps/libasync_trait-*.so \
    -L target/debug/deps \
    -o test_discord_only

if [ $? -eq 0 ]; then
    echo "Compilation successful! Running Discord test..."
    ./test_discord_only
else
    echo "Compilation failed. Using cargo instead..."
    # Fallback to cargo run
    cargo run --bin test_discord_only
fi