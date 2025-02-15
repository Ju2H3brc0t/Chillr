import discord
from discord import app_commands
from discord.ext import commands

class say(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="say", description="Make the bot say something.")
    @app_commands.describe(message="The message you want the bot to say.", channel="The channel you want the bot to say the message in.")
    async def say(self, interaction: discord.Interaction, message: str, channel: discord.TextChannel = None):
        await channel.send(message)

async def setup(bot):
    await bot.add_cog(say(bot))