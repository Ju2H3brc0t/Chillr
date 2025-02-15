import discord
from discord import app_commands
from discord.ext import commands
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

log_channel = config['command']['kick']['log_channel']

class kick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="kick", description="Kick a user from the server.")
    @app_commands.describe(user="The user to kick.")
    async def kick(self, interaction: discord.Interaction, user: discord.User):
        log_channel_id = self.bot.get_channel(log_channel)
        await log_channel_id.send(f"{interaction.user.mention} kicked {user.mention} from the server.")
        await user.kick(user)
    
async def setup(bot):
    await bot.add_cog(kick(bot))