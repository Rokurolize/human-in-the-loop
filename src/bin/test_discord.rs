use serenity::{
    all::{ChannelId, CreateMessage, EventHandler, GatewayIntents, Ready},
    async_trait, Client,
};
use std::env;

struct Handler {
    channel_id: u64,
}

#[async_trait]
impl EventHandler for Handler {
    async fn ready(&self, ctx: serenity::all::Context, ready: Ready) {
        println!("Connected as {}", ready.user.name);
        
        let channel = ChannelId::new(self.channel_id);
        match channel.send_message(&ctx.http, CreateMessage::new().content("Bot connected successfully! ✅")).await {
            Ok(_) => println!("Test message sent!"),
            Err(e) => println!("Failed to send message: {}", e),
        }
    }
}

#[tokio::main]
async fn main() {
    let token = env::var("DISCORD_TOKEN").expect("DISCORD_TOKEN not set");
    let channel_id: u64 = env::var("DISCORD_CHANNEL_ID")
        .expect("DISCORD_CHANNEL_ID not set")
        .parse()
        .expect("Invalid channel ID");
    
    println!("Starting Discord connection test...");
    println!("Channel ID: {}", channel_id);
    
    let intents = GatewayIntents::GUILD_MESSAGES | GatewayIntents::MESSAGE_CONTENT;
    let handler = Handler { channel_id };
    
    let mut client = Client::builder(&token, intents)
        .event_handler(handler)
        .await
        .expect("Failed to create client");
    
    if let Err(why) = client.start().await {
        println!("Client error: {:?}", why);
    }
}