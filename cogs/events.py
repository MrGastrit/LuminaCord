import discord
from discord.ext import commands


class EventsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        channel = self.bot.get_channel(1367128266552377418)
        embed = discord.Embed(title=f"Добро пожаловать на сервер!", description=f"Надеюсь, что ты тут надолго!\nПока можешь ознакомиться с правилами: <#1367128425503916083>", color=discord.Color.pink())
        await channel.send(content=f"{member.mention}", embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        channel = self.bot.get_channel(1367128266552377418)
        embed = discord.Embed(title=f"До встречи!", description="Возможно, ты еще вернешься", color=discord.Color.red())
        await channel.send(content=f"{member.mention}", embed=embed)

async def setup(bot):
    await bot.add_cog(EventsCog(bot))
