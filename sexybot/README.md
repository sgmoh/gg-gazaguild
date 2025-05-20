# Discord Bot

A multi-purpose Discord bot with moderation, welcome messages, reaction roles, and more.

## Features

- **Custom Emojis**: Enhanced help menu with custom Discord emojis
- **Moderation Commands**: Ban, kick, timeout, and other moderation tools
- **Channel Management**: Create, delete, and modify channels with ease
- **Welcome Messages**: Automatic welcome messages for new members
- **Reaction Roles**: Self-assignable roles with reactions
- **Red Embeds**: All embeds are styled with red color

## Setup and Deployment

### Prerequisites
- Discord Bot Token
- Python 3.8+
- PostgreSQL database (optional)

### Local Setup
1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your Discord token:
   ```
   DISCORD_TOKEN=your_token_here
   ```
4. Run the bot:
   ```
   python run_fixed_bot.py
   ```

### Deploying to Render
1. Create a new Web Service in Render
2. Connect to your GitHub repository
3. Set the build command to: `pip install -r requirements.txt`
4. Set the start command to: `python run_fixed_bot.py`
5. Add the environment variables:
   - `DISCORD_TOKEN`: Your Discord bot token
   - `DATABASE_URL`: (Optional) PostgreSQL connection string
   - `USE_POSTGRES`: true (if using PostgreSQL)
6. Deploy!

## Commands

Use `.help` to see all available commands. Here are some main command categories:

- `.help` - Shows the help menu with all commands
- `.ban` - Ban a user from the server
- `.kick` - Kick a user from the server
- `.timeout` - Put a user in timeout
- `.welcome` - Configure welcome messages
- `.reactionrole` - Set up reaction roles

## Monitoring

The bot is equipped with health checks for UptimeRobot monitoring. The health check endpoint is available at `/health`.

## Support

If you need help or have questions, join our support server: [Discord Invite](https://discord.gg/gazaguild)