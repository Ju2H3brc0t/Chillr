from discord.ext import commands
import asyncio

class on_msg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(bot, message):
        print(f"{message} sended in {message.channel}")
        try:
            if message.channel == bot.get_channel(1118160135961976965):
                try:
                    await asyncio.sleep(180)
                    await message.delete()
                except Exception as e:
                    print(f"A error has occured while deleting message: {e}")
            elif message.channel == bot.get_channel(1122777165331693678):
                await asyncio.sleep(3600)
                await message.delete()
            elif message.channel == bot.get_channel(1138880792009900082):
                await asyncio.sleep(604800)
                await message.delete()
        except Exception as e:
            print(f"A error has occured while sorting the rooms: {e}")
    
async def setup(bot):
    await bot.add_cog(on_msg(bot))