from discord.ext import commands
import asyncio

class on_msg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(bot, message):
        if message.channel == bot.get_channel(1118160135961976965):
            await asyncio.sleep(180)
            await message.delete()
        elif message.channel == bot.get_channel(1122777165331693678):
            await asyncio.sleep(3600)
            await message.delete()
        elif message.channel == bot.get_channel(1138880792009900082):
            await asyncio.sleep(604800)
            await message.delete()
    
async def setup(bot):
    await bot.add_cog(on_msg(bot))