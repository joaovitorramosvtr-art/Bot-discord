
import discord
from discord.ext import commands
from discord.ui import Button, View
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

fila = []

CANAL_DESTINO_ID = 1489312438103965877  # COLOQUE O ID DO CANAL

class FilaView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🧊 Gelo Infinito", style=discord.ButtonStyle.green)
    async def gelo_infinito(self, interaction: discord.Interaction, button: Button):
        await entrar_fila(interaction)

    @discord.ui.button(label="🧊 Gelo Normal", style=discord.ButtonStyle.primary)
    async def gelo_normal(self, interaction: discord.Interaction, button: Button):
        await entrar_fila(interaction)

    @discord.ui.button(label="❌ Sair da Fila", style=discord.ButtonStyle.red)
    async def sair(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id in fila:
            fila.remove(interaction.user.id)
            await interaction.response.send_message("Você saiu da fila!", ephemeral=True)
        else:
            await interaction.response.send_message("Você não está na fila!", ephemeral=True)

async def entrar_fila(interaction):
    if interaction.user.id in fila:
        await interaction.response.send_message("Você já está na fila!", ephemeral=True)
        return

    if len(fila) >= 2:
        await interaction.response.send_message("Fila cheia!", ephemeral=True)
        return

    fila.append(interaction.user.id)
    await interaction.response.send_message("Você entrou na fila!", ephemeral=True)

    if len(fila) == 2:
        canal = bot.get_channel(CANAL_DESTINO_ID)
        jogadores = [f"<@{id}>" for id in fila]

        await canal.send(f"🔥 PARTIDA FORMADA!\nJogadores: {', '.join(jogadores)}")

        fila.clear()

@bot.command()
async def criarfila(ctx):
    embed = discord.Embed(
        title="🔥 FILA DE APOSTADO",
        color=discord.Color.red()
    )

    embed.add_field(name="🏆 Nome da Org", value="Sua Org", inline=False)
    embed.add_field(name="💰 Valor", value="R$ 0", inline=False)
    embed.add_field(name="🎮 Modo", value="1x1 / 2x2 / 3x3 / 4x4", inline=False)
    embed.add_field(name="👥 Jogadores", value="0/2", inline=False)

    await ctx.send(embed=embed, view=FilaView())

@bot.event
async def on_ready():
    print(f"Bot online como {bot.user}")

bot.run(os.getenv("TOKEN"))
