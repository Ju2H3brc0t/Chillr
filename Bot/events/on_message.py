from discord.ext import commands
import asyncio
import json
import os
import yaml

def load_config(config_file="event_config.yaml"):
    dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(dir, config_file)

    if not os.path.exists(path):
        raise FileNotFoundError("Configuration file not found")

    with open(path, "r") as file:
        return yaml.safe_load(file)

config = load_config()

counting_channel = config['event']['counting']['channel_id']
bot_channel = config['event']['message_deletion']['channel_id']['bot']
staff_bot_channel = config['event']['message_deletion']['channel_id']['bot_staff']
bot_sleep = config['event']['message_deletion']['sleep_time']['bot']
staff_bot_sleep = config['event']['message_deletion']['sleep_time']['bot_staff']
log_sleep = config['event']['message_deletion']['sleep_time']['log']

log_channel = config['event']['message_deletion']['channel_id']['log']
file_path_count = config['event']['counting']['path']

def load_count():
    try:
        with open(file_path_count, "r") as f:
            data = json.load(f)
            return data['count']
    except (FileNotFoundError, json.JSONDecodeError):
        return 0

def save_count():
    data = {'count': count}
    with open(file_path_count, "w") as f:
        json.dump(data, f, indent=4)

count = load_count()
last_message = {}

class on_message(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        
        message_channel = message.channel.id

        try:
            if message_channel == bot_channel:
                print("Starting message deletion")
                await asyncio.sleep(bot_sleep)
                await message.delete()
                print("Message deleted")
            elif message_channel == staff_bot_channel:
                await asyncio.sleep(staff_bot_sleep)
                await message.delete()
            elif message_channel == log_channel:
                await asyncio.sleep(log_sleep)
                await message.delete()
        except Exception as e:
            print(f"An error has occured: {e}")

        global count, last_message
        if message_channel == counting_channel:
            try:
                user_count = int(message.content)
                if user_count == count + 1 and message.author.id not in last_message:
                    await message.add_reaction("✅")
                    count += 1
                    save_count()
                else:
                    await message.add_reaction("❌")
                    reason = "Le nombre envoyé est incorrect"
                    if message.author.id in last_message:
                        reason = "Vous ne pouvez pas participer deux fois de suite"
                    last_message = {message.author.id: message.content}
                    last_message.clear()
                    count = 0
                    save_count()
                    await message.channel.send(f"{message.author.mention} s'est trompé, {reason}, le compteur a été remis à zéro.")
                last_message = {message.author.id: message.content}
            except ValueError:
                await message.add_reaction("❌")
                await message.channel.send(f"{message.author.mention}, veuillez envoyer un nombre entier.")

async def setup(bot):
    await bot.add_cog(on_message(bot))