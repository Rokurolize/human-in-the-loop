use serenity::{
    all::{ChannelId, EventHandler, GatewayIntents, Ready, UserId},
    async_trait, Client,
};

struct Handler {
    channel_id: ChannelId,
    user_id: UserId,
}

#[async_trait]
impl EventHandler for Handler {
    async fn ready(&self, ctx: serenity::all::Context, ready: Ready) {
        println!("Connected as {}", ready.user.name);
        
        // Send a test message to the channel
        if let Err(why) = self.channel_id
            .say(&ctx.http, format!("Bot connected! Ready to receive questions. <@{}>", self.user_id))
            .await
        {
            println!("Error sending message: {:?}", why);
        } else {
            println!("Test message sent successfully!");
        }
    }
}

#[tokio::main]
async fn main() {
    let token = std::env::var("DISCORD_TOKEN").expect("DISCORD_TOKEN not set");
    let channel_id = std::env::var("DISCORD_CHANNEL_ID")
        .expect("DISCORD_CHANNEL_ID not set")
        .parse::<u64>()
        .expect("Invalid channel ID")
        .into();
    let user_id = std::env::var("DISCORD_USER_ID")
        .expect("DISCORD_USER_ID not set")
        .parse::<u64>()
        .expect("Invalid user ID")
        .into();

    println!("Starting Discord bot test...");
    println!("Channel ID: {}", channel_id);
    println!("User ID: {}", user_id);

    let intents = GatewayIntents::GUILD_MESSAGES | GatewayIntents::MESSAGE_CONTENT;
    let handler = Handler { channel_id, user_id };

    let mut client = Client::builder(&token, intents)
        .event_handler(handler)
        .await
        .expect("Failed to create client");

    if let Err(why) = client.start().await {
        println!("Client error: {:?}", why);
    }
}