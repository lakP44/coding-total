import discord
from discord.ext import commands


class my_bot(commands.Bot):
    def __init__(self):
        # 디스코드 봇의 명령어를 칠때 맨앞의 접두사를 결정함,
        super().__init__(command_prefix='!', intents=discord.Intents.all(), help_command=None)

    async def on_ready(self):
        print('bot 준비완료')

    async def setup_hook(self):
        await self.load_extension(f"dice")
        await self.load_extension(f"rsp")


bot = my_bot()
bot.run('MTA3NzEzMzczMzIxNzQ0Nzk5MQ.GkW0KS.3U039wzNtmpKhLmlFbmZ4EUbCHS_C26tRSNBH4')
