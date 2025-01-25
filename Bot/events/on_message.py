import discord
from discord.ext import commands
import asyncio

class on_msg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message):
        bot_channel = self.bot.get_channel(118160135961976965)
        bot_staff_channel = self.bot.get_channel(1122777165331693678)
        logs_channel = self.bot.get_channel(138880792009900082)
        message_channel = message.channel.id
        try:
            if str(message_channel) == str(bot_channel):
                await asyncio.sleep(180)
                await message.delete()
            elif str(message_channel) == str(bot_staff_channel):
                await asyncio.sleep(3600)
                await message.delete()
            elif str(message_channel) == str(logs_channel):
                await asyncio.sleep(604800)
                await message.delete()
        except Exception as e:
            print(f"A error has occured while sorting the rooms: {e}")
    
async def setup(bot):
    await bot.add_cog(on_msg(bot))