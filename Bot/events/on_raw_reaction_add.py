import discord
from discord.ext import commands
import yaml
import os

def load_config(config_file="event_config.yaml"):
    dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(dir, config_file)

    if not os.path.exists(path):
        raise FileNotFoundError("Configuration file not found")

    with open(path, "r") as file:
        return yaml.safe_load(file)

config = load_config()

poll_channel = config['event']['on_raw_reation_add']['reaction_deletion']['channel_id']['poll']

class OnRawReactionAdd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.channel_id == poll_channel and payload.user_id != self.bot.user.id:

            channel = self.bot.get_channel(payload.channel_id)
            if not channel:
                return
            message = await channel.fetch_message(payload.message_id)
            user = message.guild.get_member(payload.user_id)
            if not user:
                return
            
            for reaction in message.reactions:
                if reaction.me:
                    continue
                users = await reaction.users().flatten()
                if user in users and str(reaction.emoji) != str(payload.emoji.name):
                    await message.remove_reaction(reaction.emoji, user)
                    break