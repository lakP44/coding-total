import discord
from discord.ext import commands
import random

class Rsp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    async def rsp_play(self, message):
        ai = Rsp.rsp_dice(self) # ai는 일급함수, 
        try:
            coro = await self.bot.wait_for('message', timeout = 10)
        except:
            await message.channel.send('시간초과되었습니다.')
        else:
            if coro.content.startswith('가위'):
                if ai == '가위':
                    await message.channel.send(f'봇이 {ai}를 내서 비겼습니다.')
                elif ai == '바위':
                    await message.channel.send(f'봇이 {ai}를 내서 당신이 졌습니다.')
                elif ai == '보':
                    await message.channel.send(f'봇이 {ai}를 내서 당신이 이겼습니다.')
            elif coro.content.startswith('바위'):
                if ai == '가위':
                    await message.channel.send(f'봇이 {ai}를 내서 당신이 이겼습니다.')
                elif ai == '바위':
                    await message.channel.send(f'봇이 {ai}를 내서 비겼습니다.')
                elif ai == '보':
                    await message.channel.send(f'봇이 {ai}를 내서 당신이 졌습니다.')
            elif coro.content.startswith('보'):
                if ai == '가위':
                    await message.channel.send(f'봇이 {ai}를 내서 당신이 졌습니다.')
                elif ai == '바위':
                    await message.channel.send(f'봇이 {ai}를 내서 당신이 이겼습니다.')
                elif ai == '보':
                    await message.channel.send(f'봇이 {ai}를 내서 비겼습니다.')
                    
    def rsp_dice(self):
        dice = ['가위', '바위', '보']
        random.shuffle(dice)
        return dice.pop()
        
    @commands.Cog.listener()
    async def on_message(self, message): # 메세지를 받아오고 싶으면 무조건 이 함수를 써야함
        if message.content.startswith('rsp'): # endswith은 끝나는 메세지를 검사, startswith은 이것으로 시작하는 메세지를 검사
            await message.channel.send('가위바위보 게임을 시작합니다.')
            await Rsp.rsp_play(self, message)
            
async def setup(bot):
    await bot.add_cog(Rsp(bot))