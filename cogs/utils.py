import discord
from discord import app_commands
from discord.ext import commands

class UtilsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="poll", description="Создать опрос")
    @app_commands.describe(question="Тема опроса", option1="Вариант ответа", option2="Вариант ответа", option3="Вариант ответа", option4="Вариант ответа", option5="Вариант ответа")
    @commands.has_permissions(administrator=True)
    async def poll(self, interaction: discord.Interaction, question: str, option1: str, option2: str, option3: str = None, option4: str = None, option5: str = None):
        try:
            options = [option1, option2, option3, option4, option5]
            emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]

            embed = discord.Embed(title=f"📊 Опрос\n{question}", color=discord.Colour.blurple())

            emj = []
            for i, option in enumerate(options):
                if option:
                    emj.append(emojis[i])
                    embed.add_field(name=f"{i + 1}. {option}", value="", inline=False)

            message = await interaction.channel.send(embed=embed)

            for emoji in emj:
                await message.add_reaction(emoji)
        except Exception as e:
            print(e)

async def setup(bot):
    await bot.add_cog(UtilsCog(bot))