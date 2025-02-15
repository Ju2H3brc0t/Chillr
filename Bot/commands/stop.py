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

bot_owner_id = config['command']['stop']['user_id']['bot_owner']

counting_channel = config['command']['stop']['channel_id']['counting']
bot_channel = config['command']['stop']['channel_id']['bot']
bot_staff_channel = config['command']['stop']['channel_id']['bot_staff']
log_channel = config['command']['stop']['channel_id']['log']

class stop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="stop", description="Stop the bot.")
    async def stop(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        server_owner_id = interaction.guild.owner_id
        bot_owner_id = self.bot.get_user(bot_owner_id)

        counting_channel_id = self.bot.get_channel(counting_channel)
        bot_channel_id = self.bot.get_channel(bot_channel)
        bot_staff_channel_id = self.bot.get_channel(bot_staff_channel)
        log_channel_id = self.bot.get_channel(log_channel)
        
        if user_id == bot_owner_id or user_id == server_owner_id:
            await interaction.response.send_message("Stopping the bot...", ephemeral=True)
            print("Stopping the bot...")
        
            for role in interaction.guild.roles:
                if role.is_default():
                    continue
                await counting_channel_id.set_permissions(role, send_messages=False)
        
            await bot_channel_id.purge(limit=100)
            await bot_staff_channel_id.purge(limit=100)
            await log_channel_id.purge(limit=100)

            await self.bot.close()
            sys.exit(0)
        else:
            await interaction.response.send_message("", ephemeral=True)

async def setup(bot):
    await bot.add_cog(stop(bot))