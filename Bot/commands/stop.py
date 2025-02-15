import discord
from discord import app_commands
from discord.ext import commands
import sys
import os
import yaml

def load_config(config_file="command_config.yaml"):
    dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(dir, config_file)

    if not os.path.exists(path):
        raise FileNotFoundError("Configuration file not found")

    with open(path, "r") as file:
        return yaml.safe_load(file)

config = load_config()

counting_channel = config['command']['stop']['channel_id']['counting']

class stop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="stop", description="Stop the bot.")
    async def stop(self, ctx, interaction: discord.Interaction, channel: counting_channel):
        await interaction.response.send_message("Stopping the bot...", ephemeral=True)
        for role in ctx.guild.roles:
            if role.is_default():
                continue
            await channel.set_permissions(role, send_messages=False)
        await self.bot.close()
        sys.exit(0)

async def setup(bot):
    await bot.add_cog(stop(bot))