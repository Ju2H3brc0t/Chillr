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
counting_channel_id = int(config['event']['counting']['channel_id'])

bot_channel = int(config['event']['message_deletion']['channel_id']['bot_channel'])
staff_bot_channel = int(config['event']['message_deletion']['channel_id']['staff_bot_channel'])
log_channel = int(config['event']['message_deletion']['channel_id']['log_channel'])

class OnReady(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.wait_until_ready()
        print(f"Connecté en tant que {self.bot.user}")

        try:
            synced = await self.bot.tree.sync()
            print(f"{len(synced)} commandes synchronisées.")
        except Exception as e:
            print(f"Échec de la synchronisation des commandes : {e}")

        counting_channel = self.bot.get_channel(counting_channel_id)
        if counting_channel is None:
            return

        for role in counting_channel.guild.roles:
            if role.is_default():
                continue
            await counting_channel.set_permissions(role, send_messages=True)

        channels = [
            self.bot.get_channel(bot_channel),
            self.bot.get_channel(staff_bot_channel),
            self.bot.get_channel(log_channel)
        ]

        for channel in channels:
            if channel is None:
                continue

            while True:
                messages = await channel.history(limit=100).flatten()
                if not messages:
                    break
                await channel.delete_messages(messages)

async def setup(bot):
    await bot.add_cog(OnReady(bot))

