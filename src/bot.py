import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
from keep_alive import keep_alive

load_dotenv()

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # para detectar nuevos usuarios

bot = commands.Bot(command_prefix="!", intents=intents)

# Mantener vivo
keep_alive()

# Actividad fake para evitar sleep
async def keep_active():
    await bot.wait_until_ready()
    while not bot.is_closed():
        print("Sigo vivo 👀")
        await asyncio.sleep(300)

@bot.event
async def setup_hook():
    bot.loop.create_task(keep_active())

# Evento: bot listo
@bot.event
async def on_ready():
    print(f"Bot listo como {bot.user}")

# Bienvenida
@bot.event
async def on_member_join(member):
    channel = member.guild.system_channel
    if channel:
        await channel.send(f"Bienvenido {member.mention} 🎉")

# Comando ping
@bot.command()
async def ping(ctx):
    await ctx.send("pong 🏓")

# Crear evento
@bot.command()
async def event(ctx, *, nombre):
    mensaje = await ctx.send(f"🗓️ **Evento:** {nombre}\n\nReacciona:\n👍 = Participo\n👎 = No participo")

    await mensaje.add_reaction("👍")
    await mensaje.add_reaction("👎")

# Limpiar mensajes (admin)
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, cantidad: int):
    await ctx.channel.purge(limit=cantidad + 1)
    await ctx.send(f"{cantidad} mensajes eliminados", delete_after=5)


bot_commands = "1. ping: Verificar actividad.\n2. event [Mensaje]: Programar evento.\n"
               "3. clear [Cantidad]: Limpiar mensajes (admin).\n"


# Comandos del Bot
@bot.command()
async def help(ctx):
    await ctx.send(f"{bot_commands}")

bot.run(TOKEN)
