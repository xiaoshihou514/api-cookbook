# This code is a simplified example of a Discord bot that integrates with the Perplexity AI API. This is a complete, minimal bot script that someone can run directly. Notice I have simplified the permission logic to only check for administrators to remove the need for an external database, making the example much more focused on the Perplexity API.

# bot.py
import os
import discord
from discord.ext import commands
from discord import app_commands
import openai
from dotenv import load_dotenv

# --- Step 1: Load Environment Variables ---
# This ensures your secret keys are kept safe in a .env file.
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")

# --- Step 2: Bot Setup ---
# We define the bot's intents, which tell Discord what events our bot needs to receive.
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# --- Step 3: Create a Command Cog ---
# Cogs are how modern discord.py bots organize commands, listeners, and state.
class AIChatCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        # Initialize the Perplexity AI Client using the key from our .env file.
        # The `base_url` is the crucial part that directs the OpenAI library to Perplexity's API.
        if PERPLEXITY_API_KEY:
            self.perplexity_client = openai.OpenAI(
                api_key=PERPLEXITY_API_KEY,
                base_url="https://api.perplexity.ai"
            )
            print("Perplexity AI Client Initialized.")
        else:
            self.perplexity_client = None
            print("CRITICAL: PERPLEXITY_API_KEY not found in .env file.")

    # Define the slash command. 
    # The `has_permissions` check restricts this command to server administrators.
    @app_commands.command(name="ask_perplexity", description="Ask a question to Perplexity AI (with web access).")
    @app_commands.describe(prompt="The question you want to ask.")
    @app_commands.checks.has_permissions(administrator=True)
    async def ask_perplexity(self, interaction: discord.Interaction, prompt: str):
        if not self.perplexity_client:
            return await interaction.response.send_message(
                "The Perplexity AI service is not configured on this bot.", 
                ephemeral=True
            )

        # Defer the response to give the API time to process without a timeout.
        await interaction.response.defer(thinking=True)
        
        try:
            # Create the list of messages for the API call, following the standard format.
            messages = [{"role": "user", "content": prompt}]
            
            # Call the Perplexity API with the desired model.
            response = self.perplexity_client.chat.completions.create(
                model="sonar-pro", 
                messages=messages
            )
            
            answer = response.choices[0].message.content

            # Create and send a nicely formatted Discord embed for the response.
            embed = discord.Embed(
                title="🌐 Perplexity's Response", 
                description=answer, 
                color=discord.Color.from_rgb(0, 255, 0) # Perplexity Green
            )
            embed.set_footer(text=f"Requested by {interaction.user.display_name}")
            
            # Truncate the original prompt if it's too long to fit in an embed field.
            truncated_prompt = (prompt[:1020] + '...') if len(prompt) > 1024 else prompt
            embed.add_field(name="Your Prompt", value=f"```{truncated_prompt}```", inline=False)
            
            await interaction.followup.send(embed=embed)
            
        except Exception as e:
            # Inform the user if an error occurs.
            error_message = f"An error occurred with the Perplexity API: {e}"
            print(error_message)
            await interaction.followup.send(error_message, ephemeral=True)

    # A local error handler specifically for this command's permission check.
    @ask_perplexity.error
    async def on_ask_perplexity_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message("You must be an administrator to use this command.", ephemeral=True)
        else:
            # For other errors, print them to the console.
            print(f"An unhandled error occurred: {error}")
            # Potentially send a generic error message back to the user as well.
            if not interaction.response.is_done():
                await interaction.response.send_message("An unexpected error occurred.", ephemeral=True)


# --- Step 4: Main Bot Events and Startup Logic ---
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')
    try:
        # Add the cog to the bot so its commands are registered.
        await bot.add_cog(AIChatCog(bot))
        
        # Sync the slash commands to Discord. This makes them appear for users.
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s).")
    except Exception as e:
        print(f"Error during setup: {e}")

# This is the entry point for running the bot.
if __name__ == "__main__":
    if not DISCORD_TOKEN or not PERPLEXITY_API_KEY:
        print("CRITICAL: DISCORD_TOKEN and/or PERPLEXITY_API_KEY not found in .env file. Bot cannot start.")
    else:
        bot.run(DISCORD_TOKEN)