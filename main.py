import discord
from discord.ext import commands
from bot import bot
import asyncio
import os
from dotenv import load_dotenv

load_dotenv("important.env")

@bot.event
async def on_ready():
    print(f"{bot.user}")

async def main():
    async with bot:
        await bot.load_extension("cogs.fun")
        await bot.load_extension("cogs.admin")
        await bot.start(os.getenv("DS_TOKEN"))

asyncio.run(main())
