import discord
from discord import app_commands
from discord.ext import commands
from typing import Literal
import yaml
import os

def load_config(config_file="command_config.yaml"):
    dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(dir, config_file)

    if not os.path.exists(path):
        raise FileNotFoundError("Configuration file not found")

    with open(path, "r") as file:
        return yaml.safe_load(file)

config = load_config()

class poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="poll", description="Create a poll.")
    @app_commands.describe(question="The question you want to ask.", option = "Number of options you want to add.")
    async def poll(self, interaction: discord.Interaction, question: str, option: Literal["2", "3", "4", "5"]):
        modal = PollModal(question, int(option))
        await interaction.response.send_modal(modal)
        
class PollModal(discord.ui.Modal):
    def __init__(self, question: str, option_count: int):
        super().__init__(title="Poll")
        self.question = question
        self.option_count = option_count
        self.options = []

        for i in range(option_count):
            input_field = discord.ui.TextInput(
                label=f"Option {i + 1}",
                placeholder=f"Entre l'option {i + 1}",
                required=True,
                style=discord.TextStyle.short
            )
            self.add_item(input_field)
            self.options.append(input_field)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            poll_channel = interaction.client.get_channel(config['command']['poll']['channel_id']['poll'])

            embed = discord.Embed(
                title="🗳️ Nouveau Sondage",
                description=self.question,
                color=discord.Color.blurple()
            )

            emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]

            for i, option in enumerate(self.options):
                embed.add_field(name=emojis[i], value=option.value, inline=False)

            msg = await poll_channel.send(embed=embed)

            for i in range(self.option_count):
                await msg.add_reaction(emojis[i])

            await interaction.response.send_message("Sondage créé avec succès ✅", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Une erreur s'est produite lors de la création du sondage : {e}", ephemeral=True)
            print(f"Erreur lors de la création du sondage : {e}")


async def setup(bot):
    await bot.add_cog(poll(bot))