import os
import discord
from discord.ext import commands
import asyncio
import logging
import sys
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('discord_bot')

# Load environment variables
load_dotenv()

# Import the configuration
from config import CONFIG

def initialize_bot():
    # Set intents - we need all of them for the features we're implementing
    intents = discord.Intents.all()
    
    # Initialize the bot with prefix and intents
    bot = commands.Bot(command_prefix=CONFIG['prefix'], intents=intents, help_command=None)
    
    @bot.event
    async def on_ready():
        """Event triggered when the bot is ready and connected to Discord."""
        logger.info(f'Logged in as {bot.user.name} ({bot.user.id})')
        await bot.change_presence(activity=discord.Activity(
            type=discord.ActivityType.watching, 
            name=f"for {CONFIG['prefix']}help"
        ))
        logger.info("Bot is ready!")
    
    # Load all cogs from the config
    async def load_cogs():
        """Load all cogs from the configuration."""
        for cog_name in CONFIG['cogs']:
            try:
                await bot.load_extension(f'cogs.{cog_name}')
                logger.info(f'Loaded cog: {cog_name}')
            except Exception as e:
                logger.error(f'Failed to load cog {cog_name}: {e}')
    
    @bot.event
    async def on_connect():
        """Event triggered when the bot connects to Discord."""
        await load_cogs()
    
    @bot.event
    async def on_command_error(ctx, error):
        """Global error handler for command errors."""
        if isinstance(error, commands.CommandNotFound):
            return
        
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Missing required argument: {error.param.name}")
            return
        
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to use this command.")
            return
            
        if isinstance(error, commands.BotMissingPermissions):
            await ctx.send(f"I need the following permission(s) to execute this command: {', '.join(error.missing_permissions)}")
            return
        
        # Log the error for debugging
        logger.error(f"Command error in {ctx.command}: {error}")
        await ctx.send(f"An error occurred: {error}")
    
    return bot

async def main():
    """Start the bot"""
    try:
        # Initialize the bot
        bot = initialize_bot()
        
        # Get the token from environment variables
        token = os.getenv('DISCORD_TOKEN')
        if not token:
            logger.critical("No Discord token found!")
            sys.exit(1)
        
        # Start the bot
        logger.info("Starting bot...")
        await bot.start(token)
    except Exception as e:
        logger.critical(f"Error starting bot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Run the bot
    asyncio.run(main())