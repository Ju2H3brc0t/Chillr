import discord
from discord.ext import commands
import asyncio
import yaml
import os

bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())

def load_config(config_file="config.yaml"):
    dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(dir, config_file)

    if not os.path.exists(path):
        raise FileNotFoundError("Configuration file not found")

    with open(path, "r") as file:
        return yaml.safe_load(file)

config = load_config()

token_file_path = config["path"]["token"]
commands_file_path = config["path"]["commands"]

@bot.event
async def on_ready():
    print(f"Connected as {bot.user}.")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands.")
    except Exception as e:
        print(f"An error has occured: {e}")

async def load():
    for filename in os.listdir(commands_file_path):
        if filename.endswith('.py') and filename != "__init__.py":
            try:
                await bot.load_extension(f"commands.{filename[:-3]}")
            except Exception as e:
                print(f"A error occured: {e}")

with open(token_file_path) as file:
    token = file.read()

async def main():
    await load()
    await bot.start(token)

asyncio.run(main())