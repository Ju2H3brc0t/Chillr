import discord
from discord.ext import commands
import asyncio

class on_msg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message):
        message_channel = message.channel.id
        print(message.channel.id)
        try:
            if message_channel == discord.get_channel(118160135961976965):
                await asyncio.sleep(180)
                await message.delete()
            elif message_channel == discord.get_channel(1122777165331693678):
                await asyncio.sleep(3600)
                await message.delete()
            elif message_channel == discord.get_channel(138880792009900082):
                await asyncio.sleep(604800)
                await message.delete()
        except Exception as e:
            print(f"An error has occurred while sorting the rooms: {e}")
    
async def setup(bot):
    await bot.add_cog(on_msg(bot))