# Bot configuration settings

PREFIX = '.'  # Define the prefix that bot.py is looking for

CONFIG = {
    'prefix': '.',  # Bot command prefix
    'cogs': [
        'enhanced_help_menu',  # Use enhanced help menu that shows all commands
        # Removing conflicting cogs temporarily to make the bot work
        'welcome',
        'moderation',
        'channel_management'
    ],
    'colors': {
        'default': 0xED4245,  # Red (changed from Discord Blurple)
        'success': 0xED4245,  # Red (changed from Green)
        'error': 0xED4245,    # Red
        'warning': 0xED4245,  # Red (changed from Yellow)
        'info': 0xED4245      # Red (changed from Blue)
    },
    'emojis': {
        'success': '✅',
        'error': '❌',
        'warning': '⚠️',
        'info': 'ℹ️',
        'loading': '⏳',
        'ticket': '🎫',
        'giveaway': '🎉',
        'level': '⬆️',
        'invite': '📨',
        'message': '💬',
        'role': '👑'
    },
    'cooldowns': {
        'default': 3,  # Default cooldown in seconds
        'giveaway': 30,
        'ticket': 60
    },
    'placeholders': {
        'thumbnail_url': 'https://cdn.discordapp.com/emojis/964566755781476473.png'
    },
    'custom_gifs': {
        'welcome': 'assets/images/welcome.gif'
    },
    'levels': {
        'xp_per_message': 15,      # Base XP for each message
        'xp_randomizer': 5,        # Random bonus XP (0 to this value)
        'xp_cooldown': 60,         # Seconds between XP awards
        'level_up_channel_id': None,  # Set to a specific channel ID to send all level up notifications
                                      # If None, uses guild-specific settings from the database
        'level_roles': {}           # Roles awarded at specific levels - format: {level: role_id}
    }
}
