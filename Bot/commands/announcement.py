import discord
from discord import app_commands
from discord.ext import commands
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

class announcement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="announcement", description="Send a announcement.")
    @app_commands.describe(mention="The role to mention in the announcement.")
    async def announcement(self, interaction: discord.Interaction, mention: discord.Role):
        modal = AnnouncementModal(mention)
        await interaction.response.send_modal(modal)

class AnnouncementModal(discord.ui.Modal, title="Announcement Message"):
    def __init__(self, mention: discord.Role):
        super().__init__()
        self.mention = mention

    message = discord.ui.TextInput(
        label="Message",
        placeholder="Enter your announcement here.",
        required=True,
        style=discord.TextStyle.long
    )

    async def on_submit(self, interaction: discord.Interaction):
        announcement_channel_id = interaction.client.get_channel(config['command']['announcement']['channel_id']['announcement'])

        await announcement_channel_id.send(content=f"# __Annonce:__\n-# {self.mention.mention}\n\n{self.message.value}\n")
        await interaction.response.send_message("Your announcement has been sent.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(announcement(bot))