import discord
from discord import app_commands
from discord.ext import commands

class ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="ping", description="Test the bot's responsiveness with a game of ping-pong.")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"{interaction.user.mention} Pong 🏓 !")

async def setup(bot):
    await bot.add_cog(ping(bot))