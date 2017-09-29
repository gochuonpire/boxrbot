import discord
from discord.ext import commands
import random

description = '''A bot for ten menz'''
bot = commands.Bot(command_prefix='.', description=description)

def checkperms(ctx):
    allowed = ctx.message.author.id == '73654252970446848' or ctx.message.author.id == '73637559799910400' or ctx.message.author.id == '284232617363111936'
    return allowed

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.group(pass_context=True)
async def sendpass(ctx):
    """Sends the given password to the users in the 10man voice channel"""
    if(checkperms(ctx)):
        for server in bot.servers:
            for vc in server.channels:
                if vc.id == '362888848323117061':
                    for vm in vc.voice_members:
                        if(vm.id != ctx.message.author.id):
                            rough = ctx.message.content
                            password = rough[10:len(rough)]
                            msg = "Heres the ten-man password: **"  + password + "**\nJoin Up! :eggplant:"
                            await bot.send_message(vm, msg, tts=False)
                        if(vm.id == ctx.message.author.id):
                            rough = ctx.message.content
                            password = rough[10:len(rough)]
                            msg = "Password **" + password + "** sent successfully :thumbsup:"
                            await bot.send_message(vm, msg, tts=False)

@bot.group(pass_context=True)
async def sendmsg(ctx):
    """Posts the given message to the lobby text channel"""
    if(checkperms(ctx)):
        rough = ctx.message.content
        msg = rough[9:len(rough)]
        for server in bot.servers:
            for vc in server.channels:
                if(vc.id == '106386168593010688'):
                    await bot.send_message(vc, msg, tts=False)

@bot.group(pass_context=True)
async def checkme(ctx):
    """Checks to see if you are allowed to use commands"""
    if(checkperms(ctx)):
        await bot.send_message(ctx.message.author, 'You are allowed to use commands.')

bot.run('token')
