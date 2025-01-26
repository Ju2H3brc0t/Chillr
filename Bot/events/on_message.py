from discord.ext import commands
import asyncio
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

bot_channel = config['event']['on_message']['channel_id']['bot']
staff_bot_channel = config['event']['on_message']['channel_id']['bot_staff']
log_channel = config['event']['on_message']['channel_id']['log']

bot_sleep = config['event']['on_message']['sleep_time']['bot']
staff_bot_sleep = config['event']['on_message']['sleep_time']['bot_staff']
log_sleep = config['event']['on_message']['sleep_time']['log']

print(f"Bot Channel: {bot_channel}, Staff Bot Channel: {staff_bot_channel}, Log Channel: {log_channel},\n Bot Sleep: {bot_sleep}, Staff Bot Sleep: {staff_bot_sleep}, Log Sleep: {log_sleep}")

class on_msg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message):
        message_channel = message.channel.id

        try:
            if int(message_channel) == int(bot_channel):
                print("Starting message deletion in bot channel.")
                await asyncio.sleep(int(bot_sleep))
                message.delete()
                print("Message deleted in bot channel.")
            elif int(message_channel) == int(staff_bot_channel):
                await asyncio.sleep(int(staff_bot_channel))
                await message.delete()
            elif int(message_channel) == int(log_channel):
                await asyncio.sleep(int(log_sleep))
                await message.delete()
            else:
                print("This message is not in a bot channel, staff bot channel, or log channel.")
        except Exception as e:
            print(f"An error has occured: {e}")

    
async def setup(bot):
    await bot.add_cog(on_msg(bot))