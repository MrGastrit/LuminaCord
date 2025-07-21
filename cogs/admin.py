import discord
from discord.ext import commands
from discord import app_commands

class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def purge(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount)

    @app_commands.command(name="kick")
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

    @app_commands.command(name="ban")
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

    @app_commands.command(name="unban")
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


async def setup(bot):
    await bot.add_cog(AdminCog(bot))