import discord
from discord.ext import commands
import random


class Dice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def dice(self):
        dice1 = [i for i in range(1, 7)]
        dice2 = [i for i in range(1, 7)]

        random.shuffle(dice1)
        random.shuffle(dice2)

        a = dice1.pop()
        b = dice2.pop()

        return a, b

    @commands.command(name='주사위')  # <-- 얘는 !가 붙은 명령어만 검사
    async def play(self, ctx):
        user_id = ctx.message.author.id
        if user_id == 109695810282758144:
            await ctx.send('주사위 게임을 시작합니다.')
            a1, b1 = Dice.dice(self)

            if a1 > b1:
                await ctx.send(f'너: {a1}, 봇: {b1}')
                await ctx.send('니가 이겼습니다.')
            elif a1 < b1:
                await ctx.send(f'너: {a1}, 봇: {b1}')
                await ctx.send('니가 졌습니다.')
            else:
                await ctx.send(f'너: {a1}, 봇: {b1}')
                await ctx.send('비겼습니다.')
        else:
            await ctx.send('해킹하지마세요!')


async def setup(bot):
    await bot.add_cog(Dice(bot))

# @commands.Cog.listener() # <-- 얘는 모든 텍스트 검사

# @bot.event() # <-- Cog.listener랑 똑같음
# @bot.command() # <-- commands.command랑 똑같음

# 정리해둔것
# class dice(commands.Cog):
#     def __init__(self, bot):
#         self.bot = bot


# async def setup(bot):
#     await bot.add_cog(dice(bot))
