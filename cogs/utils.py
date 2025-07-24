from discord import app_commands
from discord.ext import commands
from collections import deque
import asyncio
import discord
import yt_dlp
import discord.voice_client



class UtilsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.is_playing = {}
        self.song_queues = {}

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        voice_client = member.guild.voice_client

        if not voice_client or not voice_client.is_connected():
            return

        voice_channel_bot = voice_client.channel

        if before.channel == voice_channel_bot and after.channel != voice_channel_bot:
            remaining_members = [m for m in voice_channel_bot.members if not m.bot]

            if len(remaining_members) == 0:
                await voice_client.disconnect()

                self.song_queues = {}

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

            embed.add_field(name="", value=f"\nАвтор: {interaction.user.mention}")

            await interaction.response.defer()
            message = await interaction.followup.send(embed=embed)

            for emoji in emj:
                await message.add_reaction(emoji)
        except Exception as e:
            print(e)

    @commands.command(name="112")
    async def emergency(self, ctx, member: discord.Member = None, reason: str = None):
        if ctx.channel.id == 1367128425503916086:
            if member is None:
                await ctx.message.delete(delay=3)
                msg = await ctx.send("Вы не указали участника, на которого хотите пожаловаться")
                await msg.delete(delay=3)
                return
            if reason is None:
                await ctx.message.delete(delay=3)
                msg = await ctx.send("Вы не указали причину жалобы")
                await msg.delete(delay=3)
                return
            if not ctx.message.attachments:
                await ctx.message.delete(delay=3)
                msg = await ctx.send("Вы не прикрепили доказательства (видео/скрин)")
                await msg.delete(delay=3)
                return

            await ctx.send(f"🚨 {ctx.author.mention} сообщил о правонарушении.\n\n👤 Подозреваемый: {member.mention}\n\n📋 Статья: {reason}\n\n🚓 Экипаж уже в пути.")

        else:
            await ctx.message.delete(delay=3)
            await ctx.send("Здесь нельзя использовать эту команду").delete(delay=3)


    @commands.command(name="play")
    async def play(self, ctx, url: str = None):
        try:
            if ctx.channel.id != 1367128266552377418:
                await ctx.message.delete(delay=3)
                msg = await ctx.send("Здесь нельзя использовать эту команду")
                await msg.delete(delay=3)
                return

            if url is None:
                await ctx.message.delete(delay=3)
                msg = await ctx.send("Вы не указали ссылку")
                await msg.delete(delay=3)
                return

            if not ctx.author.voice:
                await ctx.message.delete(delay=3)
                msg = await ctx.send("Вы не в голосовом канале")
                await msg.delete(delay=3)
                return

            guild_id = ctx.guild.id
            voice_channel = ctx.author.voice.channel

            if is_yt_link(url):
                audio_url, title = get_url(url)
            else:
                audio_url = url
                title = None

            if guild_id not in self.song_queues:
                self.song_queues[guild_id] = deque()
            self.song_queues[guild_id].append(audio_url)

            voice_client = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
            if not voice_client or not voice_client.is_connected():
                voice_client = await voice_channel.connect()
            elif voice_client.channel != voice_channel:
                await voice_client.move_to(voice_channel)

            await ctx.send(f"🎶 Добавлено в очередь: {url}")

            if not self.is_playing.get(guild_id, False):
                self.is_playing[guild_id] = True

                while self.song_queues[guild_id]:
                    current = self.song_queues[guild_id].popleft()
                    voice_client.play(discord.FFmpegPCMAudio(current))
                    await ctx.send(f"▶️ Сейчас играет: {title or url}")

                    while voice_client.is_playing():
                        await asyncio.sleep(1)

                self.is_playing[guild_id] = False
                await voice_client.disconnect()

        except Exception as e:
            print(f"[ERROR] {e}")

            await ctx.send("⚠️ Ошибка воспроизведения")

    @commands.command(name="stop")
    async def stop(self, ctx):
        voice_client = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        await voice_client.disconnect()

    @commands.command(name="skip")
    async def skip(self, ctx):
        voice_client = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

        guild_id = ctx.guild.id
        current = self.song_queues[guild_id].popleft()
        voice_client.stop()
        voice_client.play(discord.FFmpegPCMAudio(current))

async def setup(bot):
    await bot.add_cog(UtilsCog(bot))


def get_url(url):
    ydl_opts = {'format': 'bestaudio/best', 'quiet': True, 'noplaylist': True, 'extract_flat': False,}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info['url'], info.get('title', 'Неизвестное видео')

def is_yt_link(url: str) -> bool:
    return "youtube.com" in url or "youtu.be" in url
