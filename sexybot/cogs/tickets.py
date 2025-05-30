import discord
from discord.ext import commands
import logging
import asyncio

from utils.database import db
from utils.embed_creator import EmbedCreator
from config import CONFIG

logger = logging.getLogger('discord_bot')

class TicketButton(discord.ui.Button):
    """Button for creating tickets"""
    def __init__(self, label="Create Ticket", emoji="🎫"):
        super().__init__(
            label=label,
            emoji=emoji,
            style=discord.ButtonStyle.primary,
            custom_id="create_ticket"
        )
    
    async def callback(self, interaction):
        """Handle button click to create a ticket"""
        guild = interaction.guild
        member = interaction.user
        
        # Check if user already has an open ticket
        # This assumes tickets are channels with a naming pattern 'ticket-{user_id}'
        ticket_name = f"ticket-{member.id}"
        existing_ticket = discord.utils.get(guild.text_channels, name=ticket_name)
        
        if existing_ticket:
            await interaction.response.send_message(
                f"You already have an open ticket: {existing_ticket.mention}",
                ephemeral=True
            )
            return
            
            # Try to use ticket GIF if available
            try:
                import os
                gif_path = os.path.join("assets", "images", "tickets.gif")
                if os.path.exists(gif_path) and os.path.getsize(gif_path) > 0:
                    file = discord.File(gif_path, filename="tickets.gif")
                    embed.set_image(url="attachment://tickets.gif")
                    await ctx.send(file=file, embed=embed, view=TicketView())
                    return
            except Exception as e:
                logger.error(f"Error loading ticket GIF: {e}")
                
            # If no GIF or error, send without GIF
            view = TicketView()
            
            # Send the ticket message
            await ctx.send(embed=embed, view=view)
    
    @commands.Cog.listener()
    async def on_interaction(self, interaction):
        """Handle interactions for ticket buttons"""
        if not interaction.type == discord.InteractionType.component:
            return
        
        # Handle close ticket button
        if interaction.data.get('custom_id') == 'close_ticket':
            # Check if this is a ticket channel
            ticket_data = db.get_ticket(interaction.guild.id, interaction.channel.id)
            if not ticket_data:
                await interaction.response.send_message(
                    "This is not a ticket channel.",
                    ephemeral=True
                )
                return
            
            # Check permissions
            if not interaction.user.guild_permissions.manage_channels and \
               str(interaction.user.id) != ticket_data.get('user_id'):
                await interaction.response.send_message(
                    "You don't have permission to close this ticket.",
                    ephemeral=True
                )
                return
            
            # Update database
            db.close_ticket(interaction.guild.id, interaction.channel.id)
            
            # Send closing message
            await interaction.response.send_message(
                f"🔒 Ticket closed by {interaction.user.mention}. This channel will be deleted in 5 seconds.",
                ephemeral=False
            )
            
            # Wait and delete the channel
            await asyncio.sleep(5)
            try:
                await interaction.channel.delete(reason=f"Ticket closed by {interaction.user}")
            except discord.Forbidden:
                await interaction.channel.send("I don't have permission to delete this channel.")
            except discord.HTTPException as e:
                logger.error(f"Error deleting ticket channel: {e}")
    
    @commands.hybrid_command(name="close", description="Close a ticket")
    async def close(self, ctx):
        """Close a ticket channel"""
        # Check if this is a ticket channel
        ticket_data = db.get_ticket(ctx.guild.id, ctx.channel.id)
        if not ticket_data:
            embed = EmbedCreator.create_error_embed(
                "Not a Ticket",
                "This command can only be used in ticket channels."
            )
            await ctx.send(embed=embed)
            return
        
        # Check permissions
        if not ctx.author.guild_permissions.manage_channels and \
           str(ctx.author.id) != ticket_data.get('user_id'):
            embed = EmbedCreator.create_error_embed(
                "Permission Denied",
                "You don't have permission to close this ticket."
            )
            await ctx.send(embed=embed)
            return
        
        # Update database
        db.close_ticket(ctx.guild.id, ctx.channel.id)
        
        # Send closing message
        embed = EmbedCreator.create_success_embed(
            "Ticket Closing",
            f"Ticket closed by {ctx.author.mention}. This channel will be deleted in 5 seconds."
        )
        await ctx.send(embed=embed)
        
        # Wait and delete the channel
        await asyncio.sleep(5)
        try:
            await ctx.channel.delete(reason=f"Ticket closed by {ctx.author}")
        except discord.Forbidden:
            await ctx.send("I don't have permission to delete this channel.")
        except discord.HTTPException as e:
            logger.error(f"Error deleting ticket channel: {e}")

class Tickets(commands.Cog):
    """Ticket system for support"""
    
    def __init__(self, bot):
        self.bot = bot
        logger.info("Tickets cog initialized")
        
    @commands.command(name="ticket", help="Create a support ticket")
    async def ticket(self, ctx):
        """Create a support ticket"""
        # Implementation will go here
        await ctx.send("This command is under development. Please try again later.")

async def setup(bot):
    await bot.add_cog(Tickets(bot))
