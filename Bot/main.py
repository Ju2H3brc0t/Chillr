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
event_file_path = config["path"]["events"]

async def load_commands():
    for filename in os.listdir(commands_file_path):
        if filename.endswith('.py') and filename != "__init__.py":
            try:
                await bot.load_extension(f"commands.{filename[:-3]}")
            except Exception as e:
                print(f"A error has occured: {e}")

async def load_events():
    for filename in os.listdir(event_file_path):
        if filename.endswith('.py') and filename != "__init__.py":
            try:
                await bot.load_extension(f"events.{filename[:-3]}")
            except Exception as e:
                print(f"A error has occured: {e}")

with open(token_file_path) as file:
    token = file.read()

async def main():
    await load_commands()
    await load_events()
    await bot.start(token)

asyncio.run(main())