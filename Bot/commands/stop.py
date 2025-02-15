import discord
from discord import app_commands
from discord.ext import commands

class stop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="stop", description="Stop the bot.")
    async def stop(self, interaction: discord.Interaction):
        await interaction.response.send_message("Stopping the bot...", ephemeral=True)
        await self.bot.close()

async def setup(bot):
    await bot.add_cog(stop(bot))