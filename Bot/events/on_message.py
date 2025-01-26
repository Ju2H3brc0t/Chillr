from discord.ext import commands
import asyncio

class on_msg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message):
        message_channel = message.channel.id
        bot_channel = 1118160135961976965
        staff_bot_channel = 1122777165331693678
        log_channel = 1138880792009900082

        if message_channel == bot_channel:
            await asyncio.sleep(180)
            message.delete()
        elif message_channel == staff_bot_channel:
            await asyncio.sleep(3600)
            await message.delete()
        elif message_channel == log_channel:
            await asyncio.sleep(604800)
            await message.delete()

    
async def setup(bot):
    await bot.add_cog(on_msg(bot))