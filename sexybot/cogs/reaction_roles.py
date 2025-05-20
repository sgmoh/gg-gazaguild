import discord
from discord.ext import commands
import logging
import asyncio

from utils.database import db
from utils.embed_creator import EmbedCreator
from config import CONFIG

logger = logging.getLogger('discord_bot')

class RoleSelect(discord.ui.Select):
    """Dropdown for selecting roles"""
    def __init__(self, roles):
        options = []
        self.roles = roles
        
        for role_id, label in roles.items():
            options.append(discord.SelectOption(label=label, value=role_id))
            
        super().__init__(placeholder="Select a role...", min_values=1, max_values=1, options=options)
    
    async def callback(self, interaction):
        """Handle role selection"""
        role_id = self.values[0]
        role = interaction.guild.get_role(int(role_id))
        
        if not role:
            await interaction.response.send_message("Role not found. It may have been deleted.", ephemeral=True)
            return
            
        member = interaction.user
        
        if role in member.roles:
            await member.remove_roles(role)
            await interaction.response.send_message(f"Removed the {role.name} role.", ephemeral=True)
        else:
            await member.add_roles(role)
            await interaction.response.send_message(f"Added the {role.name} role.", ephemeral=True)
    
class ReactionRoles(commands.Cog):
    """Reaction role system for self-assignable roles"""
    
    def __init__(self, bot):
        self.bot = bot
        logger.info("ReactionRoles cog initialized")
        
    @commands.group(name="reactionrole", aliases=["rr"], invoke_without_command=True)
    @commands.has_permissions(manage_roles=True)
    async def reactionrole(self, ctx):
        """Manage reaction roles for the server"""
        embed = discord.Embed(
            title="Reaction Roles",
            description="Use the subcommands below to manage reaction roles:",
            color=CONFIG['colors']['default']
        )
        
        embed.add_field(
            name=f"`{CONFIG['prefix']}reactionrole create`",
            value="Create a new reaction role message",
            inline=False
        )
        
        embed.add_field(
            name=f"`{CONFIG['prefix']}reactionrole delete <message_id>`",
            value="Delete a reaction role message",
            inline=False
        )
        
        embed.add_field(
            name=f"`{CONFIG['prefix']}reactionrole list`",
            value="List all reaction role messages",
            inline=False
        )
        
        await ctx.send(embed=embed)
    
    @commands.command(name="listreactionroles", description="List all reaction role messages")
    @commands.has_permissions(manage_roles=True)
    async def list_roles(self, ctx):
        """List all reaction role messages in the server"""
        reaction_roles = db.data.get('reaction_roles', {}).get(str(ctx.guild.id), {})
        
        if not reaction_roles:
            embed = EmbedCreator.create_info_embed(
                "No Reaction Roles",
                "This server has no reaction role messages."
            )
            await ctx.send(embed=embed)
            return
        
        embed = discord.Embed(
            title="Reaction Role Messages",
            description="Here are all the reaction role messages in this server:",
            color=CONFIG['colors']['default']
        )
        
        for message_id, roles in reaction_roles.items():
            role_count = len(roles)
            
            # Try to get the channel
            channel_id = None
            for channel in ctx.guild.text_channels:
                try:
                    message = await channel.fetch_message(int(message_id))
                    channel_id = channel.id
                    break
                except (discord.NotFound, discord.Forbidden, discord.HTTPException):
                    continue
            
            channel_text = f"<#{channel_id}>" if channel_id else "Unknown channel"
            
            embed.add_field(
                name=f"Message ID: {message_id}",
                value=f"Channel: {channel_text}\nRoles: {role_count}",
                inline=False
            )
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(ReactionRoles(bot))
