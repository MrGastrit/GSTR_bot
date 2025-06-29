from discord.ext import commands
import discord
from random import randint
import psycopg2
import requests
import os
from dotenv import load_dotenv

load_dotenv("important.env")


conn = psycopg2.connect(user=os.getenv("user"), password=os.getenv("password"), host="localhost", port="5432", database=os.getenv("database"))
cursor = conn.cursor()


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #random
    @commands.command()
    async def random(self, ctx, int1: int, int2: int):
        await ctx.send(randint(int1, int2))

    #best quote
    @commands.command()
    async def bq_set(self, ctx, *, string=None):
        try:
            member = ctx.author

            if string is None:
                await ctx.send("Укажи текст цитаты.")
                return

            cursor.execute("INSERT INTO quotes (id, phrase) VALUES (%s, %s) ON CONFLICT (id) DO UPDATE SET phrase = EXCLUDED.phrase", (str(member.id), string))

            conn.commit()
            await ctx.send("Цитата добавлена.")
        except Exception as e:
            print(e)

    @commands.command()
    async def bq(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author

        cursor.execute("SELECT phrase FROM quotes WHERE id = %s", (str(user.id),))
        quote = cursor.fetchone()

        if not quote:
            await ctx.send("Цитата не найдена.")
            return

        await ctx.send(quote[0])

    #weather
    @commands.command()
    async def weather(self, ctx, city: str = None):
        api = "976515b0d85b4198b59120257252606"
        url = f"http://api.weatherapi.com/v1/current.json?key={api}&q={city}&lang=ru"

        if city is None:
            await ctx.send("❌ Укажи город")
            return

        data = requests.get(url).json()

        if "error" in data:
            await ctx.send(f"Ошибка: {data['error']['message']}")
            return

        location = data['location']['name']
        temp = data['current']['temp_c']
        condition = data['current']['condition']['text']
        feelslike = data['current']['feelslike_c']
        humidity = data['current']['humidity']
        wind = data['current']['wind_kph']

        await ctx.send(
            f"**Погода в {location}:**\n"
            f"Температура: {temp}°C\n"
            f"Ощущается как: {feelslike}°C\n"
            f"Влажность: {humidity}%\n"
            f"Ветер: {wind} км/ч\n"
            f"Условия: {condition}"
        )

    #other
    @commands.command()
    async def лысый(self, ctx):
        await ctx.send("<:emoji_8:1378106615458168992>")

    @commands.command()
    async def секс(self, ctx):
        await ctx.send("<:emoji_8:1376254517951070300>")

async def setup(bot):
    await bot.add_cog(Fun(bot))
