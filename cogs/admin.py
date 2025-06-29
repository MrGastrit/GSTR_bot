from discord.ext import commands
import discord
import psycopg2
from difflib import SequenceMatcher
import os
from dotenv import load_dotenv

load_dotenv("important.env")


conn = psycopg2.connect(user=os.getenv("user"), password=os.getenv("password"), host="localhost", port="5432", database=os.getenv("database"))
cursor = conn.cursor()

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    #reps
    reps_roles = [
        1387764163694166136, #0
        1387764982388887632, #1
        1387765494316269618, #2
        1387765953487699968, #3
        1387766440362512486, #4
    ]

    @commands.command()
    @commands.has_role("Главный гомик")
    async def rep(self, ctx, user: discord.Member = None):
        try:
            if user is None:
                user = ctx.author

            cursor.execute("SELECT reps FROM quotes WHERE id = %s", (str(user.id),))
            result = cursor.fetchone()

            if result:
                cursor.execute("UPDATE quotes SET reps = reps + 1 WHERE id = %s", (str(user.id),))
            else:
                cursor.execute("INSERT INTO quotes (id, reps) VALUES (%s, %s)", (str(user.id), 1))

            cursor.execute("SELECT reps FROM quotes WHERE id = %s", (str(user.id),))
            res = cursor.fetchone()
            reps_count = res[0] if res else 0

            if reps_count > 0:
                await user.add_roles(ctx.guild.get_role(self.reps_roles[1]))
                await user.remove_roles(ctx.guild.get_role(self.reps_roles[0]))

            if reps_count > 4:
                await user.add_roles(ctx.guild.get_role(self.reps_roles[2]))
                await user.remove_roles(ctx.guild.get_role(self.reps_roles[1]))

            if reps_count > 14:
                await user.add_roles(ctx.guild.get_role(self.reps_roles[3]))
                await user.remove_roles(ctx.guild.get_role(self.reps_roles[2]))

            if reps_count > 24:
                await user.add_roles(ctx.guild.get_role(self.reps_roles[4]))
                await user.remove_roles(ctx.guild.get_role(self.reps_roles[3]))

            conn.commit()
            await ctx.send(f"✅ Респект выдан {user.mention}.")
        except Exception as e:
            print(e)

    @commands.command()
    @commands.has_role("Главный гомик")
    async def minusrep(self, ctx, user: discord.Member = None):
        try:
            if user is None:
                user = ctx.author

            cursor.execute("SELECT reps FROM quotes WHERE id = %s", (str(user.id),))
            result = cursor.fetchone()

            if result:
                cursor.execute("UPDATE quotes SET reps = reps - 1 WHERE id = %s", (str(user.id),))
            else:
                cursor.execute("INSERT INTO quotes (id, reps) VALUES (%s, %s)", (str(user.id), -1))

            cursor.execute("SELECT reps FROM quotes WHERE id = %s", (str(user.id),))
            res = cursor.fetchone()
            reps_count = res[0] if res else 0

            if reps_count < 1:
                target_role_id = self.reps_roles[0]
            elif reps_count < 5:
                target_role_id = self.reps_roles[1]
            elif reps_count < 15:
                target_role_id = self.reps_roles[2]
            elif reps_count < 25:
                target_role_id = self.reps_roles[3]
            else:
                target_role_id = self.reps_roles[4]

            target_role = ctx.guild.get_role(target_role_id)

            for r_id in self.reps_roles:
                role_obj = ctx.guild.get_role(r_id)
                if role_obj != target_role and role_obj in user.roles:
                    await user.remove_roles(role_obj)

            if target_role not in user.roles:
                await user.add_roles(target_role)

            conn.commit()
            await ctx.send(f"❌ Респект отнят у {user.mention}.")

        except Exception as e:
            print(e)

    @commands.command()
    @commands.has_role("Главный гомик")
    async def repscount(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author

        cursor.execute("SELECT reps FROM quotes WHERE id = %s", (str(user.id),))
        result = cursor.fetchone()

        reps = result[0] if result else 0
        await ctx.send(f"📊 Кол-во респектов у {user.mention}: {reps}")

    #staff role
    @commands.command()
    @commands.has_role("ШЕФ")
    async def stuff(self, ctx, user: discord.Member = None):
        await user.add_roles(ctx.guild.get_role(1387758601451606156))
        await ctx.send("✅ Роль выдана")

    @commands.command()
    @commands.has_role("ШЕФ")
    async def creator(self, ctx, user: discord.Member, creator_role: str = None):
        try:
            roles = {
                "coder": 1387827939294449745,
                "musician": 1387829389412143237,
                "modeller": 1387829070955282584,
                "builder": 1387828671313870959,
            }

            if creator_role is None:
                await ctx.send("❌ Укажи название роли")
                return

            for role in roles:
                ratio = SequenceMatcher(None, creator_role, role).ratio()
                if ratio > 0.7:
                    await user.add_roles(ctx.guild.get_role(roles[role]))
                    await ctx.send("✅ Роль выдана")
                    break
                else:
                    await ctx.send("❌ Такой роли не существует")
                    break

        except Exception as e:
            print(e)

async def setup(bot):
    await bot.add_cog(Admin(bot))

