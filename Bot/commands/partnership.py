import discord
from discord import app_commands
from discord.ext import commands
import datetime
import os
import yaml

def load_config(config_file="command_config.yaml"):
    dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(dir, config_file)

    if not os.path.exists(path):
        raise FileNotFoundError("Configuration file not found")

    with open(path, "r") as file:
        return yaml.safe_load(file)

config = load_config()

class partnership(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="partnership", description="Send a partnership message.")
    @app_commands.describe(mention="The role to mention in the partnership message.", responsible="The user responsible of the partnership message.", representative="The user representative of the partnership message.")
    async def partnership(self, interaction: discord.Interaction, mention: discord.Role, responsible: discord.User, representative: discord.User):
        modal = PartnershipModal(mention, responsible, representative)
        await interaction.response.send_modal(modal)

class PartnershipModal(discord.ui.Modal, title="Partnership Message"):
    def __init__(self, mention: discord.Role, responsible: discord.User, representative: discord.User):
        super().__init__()
        self.mention = mention
        self.responsible = responsible
        self.representative = representative

    message = discord.ui.TextInput(
        label="Message",
        placeholder="Enter your partnership message here.",
        required=True,
        style=discord.TextStyle.long
    )

    async def on_submit(self, interaction: discord.Interaction):
        partnership_channel_id = interaction.client.get_channel(config['command']['partnership']['channel_id']['partnership'])

        embed = discord.Embed(colour=0xffff00, timestamp=datetime.datetime.now())
        embed.add_field(name="**Représentant:**", value=self.representative.mention, inline=False)
        embed.add_field(name="**Responsable:**", value=self.responsible.mention, inline=False)
        embed.set_footer(text="Partenariat")

        await partnership_channel_id.send(content=f"# __Partenariats:__\n-# {self.mention.mention}", embed=embed)

async def setup(bot):
    await bot.add_cog(partnership(bot))
