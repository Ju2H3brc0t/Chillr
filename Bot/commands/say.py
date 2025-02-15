import discord
from discord import app_commands
from discord.ext import commands

class say(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="say", description="Make the bot say something.")
    @app_commands.option(name="message", description="The message you want the bot to say.", type=app_commands.OptionType.STRING, required=True)
    @app_commands.option(name="channel", description="The channel you want the bot to say the message in.", type=app_commands.OptionType.CHANNEL, required=False)
    async def say(self, interaction: discord.Interaction, message: str):
        await interaction.response.send_message(message)

async def setup(bot):
    await bot.add_cog(say(bot))