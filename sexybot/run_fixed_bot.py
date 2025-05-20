import os
import sys
import asyncio
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('bot_launcher')

# Make sure we're in the right directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

# Import the uptime monitoring for Render compatibility
from uptime_monitor import run_uptime_monitor, start_stats_updater

# Initialize the uptime monitor for UptimeRobot
run_uptime_monitor()
start_stats_updater()

# Import the bot initialization function
from bot import initialize_bot

async def main():
    """Initialize and start the Discord bot"""
    try:
        # Initialize the bot
        bot = initialize_bot()
        
        # Get the token from environment variables
        token = os.getenv('DISCORD_TOKEN')
        if not token:
            logger.critical("No Discord token found in environment variables!")
            print("Please set a DISCORD_TOKEN environment variable with your bot token.")
            return
        
        # Start the bot
        logger.info("Starting Discord bot...")
        await bot.start(token)
    except Exception as e:
        logger.critical(f"Error starting bot: {e}")
        print(f"Error starting bot: {e}")

if __name__ == "__main__":
    # Run the bot
    asyncio.run(main())