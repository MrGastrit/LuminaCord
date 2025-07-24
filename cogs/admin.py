import discord
from discord.ext import commands
from discord import app_commands
import datetime

class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def purge(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount)

    @app_commands.command(name="kick", description="Выгнать участника с сервера")
    @app_commands.describe(member="Пользователь", reason="Причина")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str="Не указана"):
        try:
            await member.kick(reason=reason)

            embed = discord.Embed()
            embed.add_field(name="", value=f"Участник {member.mention} был **выгнан** с сервера\n\nПричина: {reason}\n\nВыгнал: {interaction.user.mention}")

            await interaction.response.send_message(embed=embed)

        except Exception as e:
            print(e)

    @app_commands.command(name="ban", description="Забанить участника сервера")
    @app_commands.describe(member="Пользователь", reason="Причина")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str="Не указана"):
        try:
            await member.ban(reason=reason)

            embed = discord.Embed()
            embed.add_field(name="", value=f"Участник {member.mention} был **забанен**\n\nПричина: {reason}\n\nЗабанил: {interaction.user.mention}")

            await interaction.response.send_message(embed=embed)

        except Exception as e:
            print(e)

    @app_commands.command(name="unban", description="Разбанить пользователя"
                                                    "")
    @app_commands.describe(user="ID/Имя")
    @app_commands.checks.has_permissions(ban_members=True)
    async def unban(self, interaction: discord.Interaction, user: str, reason: str="Не указана"):
        try:
            banned = interaction.guild.bans()

            async for entry in banned:
                unbanned_user = entry.user

                await interaction.guild.unban(unbanned_user)

                embed = discord.Embed()
                embed.add_field(name="", value=f"Пользователь {unbanned_user.mention} **разбанен**\n\nПричина: {reason}\n\nРазбанил: {interaction.user.mention}")

                await interaction.response.send_message(embed=embed)

        except discord.NotFound:
            await interaction.response.send_message("Пользователь не найден")
        except Exception as e:
            print(e)

    @app_commands.command(name="mute", description="Выдать мьют")
    @app_commands.describe(member="Участник", duration="Длительность", reason="Причина")
    @app_commands.checks.has_permissions(mute_members=True)
    async def mute(self, interaction: discord.Interaction, member: discord.Member, duration: str = "10m", reason: str = "Не указана"):
        try:
            until = datetime.timedelta(minutes=10)

            embed = discord.Embed(color=discord.Color.dark_teal())
            embed.add_field(name="", value=f"Пользователь {member.mention} **замьючен**", inline=False)
            embed.add_field(name="Причина", value=reason, inline=True)

            if duration[-1] == "m":
                until = datetime.timedelta(minutes=int(duration[:-1]))
                word = plural(duration[:-1], ("минута", "минуты", "минут"))
                embed.add_field(name="Срок наказания", value=f"{duration[:-1]} {word}", inline=True)
            if duration[-1] == "h":
                until = datetime.timedelta(hours=int(duration[:-1]))
                word = plural(duration[:-1], ("час", "часа", "часов"))
                embed.add_field(name="Срок наказания", value=f"{duration[:-1]} {word}", inline=True)
            if duration[-1] == "d":
                until = datetime.timedelta(days=int(duration[:-1]))
                word = plural(duration[:-1], ("день", "дня", "дней"))
                embed.add_field(name="Срок наказания", value=f"{duration[:-1]} {word}", inline=True)
            else:
                await interaction.response.send_message("Неверный формат времени", ephemeral=True)
                return

            embed.add_field(name="", value=f"Выдал: {interaction.user.mention}", inline=False)

            await member.timeout(until, reason=reason)
            await interaction.response.send_message(embed=embed)

        except Exception as e:
            print(e)


async def setup(bot):
    await bot.add_cog(AdminCog(bot))


def plural(n, forms):
    n = abs(int(n)) % 100
    n1 = n % 10
    if 11 <= n <= 19:
        return forms[2]
    if 1 == n1:
        return forms[0]
    if 2 <= n1 <= 4:
        return forms[1]
    return forms[2]