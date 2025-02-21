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
counting_channel_id = int(config['event']['on_ready']['counting']['channel_id'])

bot_channel_id = int(config['event']['on_ready']['channel_id']['bot'])
bot_staff_channel_id = int(config['event']['on_ready']['channel_id']['bot_staff'])
log_channel_id = int(config['event']['on_ready']['channel_id']['log'])

class OnReady(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.wait_until_ready()
        print(f"Connected as {self.bot.user}")

        try:
            synced = await self.bot.tree.sync()
            print(f"Synced {len(synced)} commands.")
        except Exception as e:
            print(f"Failed to sync commands: {e}")

        log_channel = self.bot.get_channel(log_channel_id)

        counting_channel = self.bot.get_channel(counting_channel_id)
        if counting_channel is None:
            return

        for role in counting_channel.guild.roles:
            if role.is_default():
                continue
            await counting_channel.set_permissions(role, send_messages=True)

        bot_channel = self.bot.get_channel(bot_channel_id)
        bot_staff_channel = self.bot.get_channel(bot_staff_channel_id)

        if bot_channel:
            await bot_channel.purge(limit=100)
        if bot_staff_channel:
            await bot_staff_channel.purge(limit=100)
        if log_channel:
            await log_channel.purge(limit=100)

        print("Bot is ready.")
        if log_channel:
            await log_channel.send("Bot is ready.")

async def setup(bot):
    cog = OnReady(bot)
    await bot.add_cog(cog)