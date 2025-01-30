from discord.ext import commands
import asyncio
import yaml
import json
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
counting_channel = config['event']['on_message']['channel_id']['counting']

bot_sleep = config['event']['on_message']['sleep_time']['bot']
staff_bot_sleep = config['event']['on_message']['sleep_time']['bot_staff']
log_sleep = config['event']['on_message']['sleep_time']['log']

file_path_count = config['event']['on_message']['path']['count']

def load_count():
    try:
        with open(file_path_count, "r") as f:
            data = json.load(f)
            return data['count']
    except FileNotFoundError:
        return 0
    except json.JSONDecodeError:
        return 0

def save_count():
    data = {'count' : count}
    with open(file_path_count, "w") as f:
        json.dump(data, f, intent=4)

count = load_count()

class on_msg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message):
        message_channel = message.channel.id

        if int(message_channel) == int(bot_channel):
            await asyncio.sleep(int(bot_sleep))
            await message.delete()
        elif int(message_channel) == int(staff_bot_channel):
            await asyncio.sleep(int(staff_bot_channel))
            await message.delete()
        elif int(message_channel) == int(log_channel):
            await asyncio.sleep(int(log_sleep))
            await message.delete()
        
        global count
        global last_message
        if message_channel == counting_channel and message.author != self.bot.user:
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
                    count = 0
                    save_count()
                    await message.channel.send(f"{message.author.mention} s'est trompé, {reason}, le compteur a été remis à zéro.")
                last_message = {message.author.id: message.content}
            except ValueError:
                await message.add_reaction("❌")
                await message.channel.send(f"{message.author.mention} le message envoyé n'est pas un nombre, le compteur est a {count}")
            except Exception as e:
                print(f"An error has occured: {e}")
    
async def setup(bot):
    await bot.add_cog(on_msg(bot))