import discord
from discord.ext import commands

class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def purge(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount)

async def setup(bot):
    await bot.add_cog(AdminCog(bot))