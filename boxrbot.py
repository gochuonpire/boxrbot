import discord
from discord.ext import commands
import random
import asyncio
from twitch import TwitchClient
from tinydb import TinyDB, Query
from tinydb.operations import delete

description = '''A bot for the boxr discord'''
bot = commands.Bot(command_prefix='.', description=description)

db = TinyDB('data.json')
Users = Query()

def checkperms(ctx):
    allowed = ctx.message.author.id == '73654252970446848' or ctx.message.author.id == '73637559799910400' or ctx.message.author.id == '284232617363111936'
    return allowed

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command(pass_context=True)
async def sendpass(ctx):
    """Sends the given password to the users in the 10man voice channel"""
    if(checkperms(ctx)):
        vc = bot.get_channel('362888848323117061')
        for vm in vc.voice_members:
            if(vm.id != ctx.message.author.id):
                rough = ctx.message.content
                password = rough[10:len(rough)]
                msg = "Heres the ten-man password: **"  + password + "**\nJoin Up! :eggplant:"
                await bot.send_message(vm, msg, tts=False)
            else:
                rough = ctx.message.content
                password = rough[10:len(rough)]
                msg = "Password **" + password + "** sent successfully :thumbsup:"
                await bot.send_message(vm, msg, tts=False)

@bot.command(pass_context=True)
async def sendmsg(ctx):
    """Posts the given message to the lobby text channel"""
    if(checkperms(ctx)):
        rough = ctx.message.content
        msg = rough[9:len(rough)]
        vc = bot.get_channel('106386168593010688')
        await bot.send_message(vc, msg, tts=False)

@bot.command(pass_context=True)
async def checkme(ctx):
    """Checks to see if you are allowed to use commands"""
    if(checkperms(ctx)):
        await bot.send_message(ctx.message.author, 'You are allowed to use commands.')

@bot.command(pass_context=True)
async def subscribe(ctx):
    """Adds you to the updatelist"""
    if db.contains(Users.id == ctx.message.author.id):
        if db.contains((Users.id == ctx.message.author.id) & (Users.sup == 0)):
            db.update({'sup': 1}, Users.id == ctx.message.author.id)
            msg = "You have been added to the notification list. We will notify you when launders is live!:thumbsup:\nTo remove yourself from this list, type .unsubscribe!"
            await bot.send_message(ctx.message.author, msg, tts=False)
        elif db.contains((Users.id == ctx.message.author.id) & (Users.sup == 1)):
            msg = "You are already subscribed to streaming notifications!:thumbsup:\nTo remove yourself from this list, type .unsubscribe!"
            await bot.send_message(ctx.message.author, msg, tts=False)
    else:
        db.insert({'id': ctx.message.author.id, 'sup': 1})
        msg = "You have been added to the notification list. We will notify you when launders is live!:thumbsup:\nTo remove yourself from this list, type .unsubscribe!"
        await bot.send_message(ctx.message.author, msg, tts=False)

@bot.command(pass_context=True)
async def unsubscribe(ctx):
    """Removes you from the updatelist"""
    if db.contains(Users.id == ctx.message.author.id):
        if db.contains((Users.id == ctx.message.author.id) & (Users.sup == 0)):
            msg = "You already aren't subscribed to streaming notifications!\nTo receive notifications again, type .subscribe!"
            await bot.send_message(ctx.message.author, msg, tts=False)
        elif db.contains((Users.id == ctx.message.author.id) & (Users.sup == 1)):
            db.update({'sup' : 0}, Users.id == ctx.message.author.id)
            msg = "You have been removed from the update list. We will no longer notify you when launders is live!"
            await bot.send_message(ctx.message.author, msg, tts=False)
    else:
        msg = "You already aren't subscribed to streaming notifications!\nTo receive notifications, type .subscribe!"
        await bot.send_message(ctx.message.author, msg, tts=False)

@bot.command(pass_context=True)
async def fill(ctx):
    """Fills 10man channel with people from waiting room"""
    server = bot.get_server('106386168593010688')
    if(checkperms(ctx)):
        rough = ctx.message.content
        pw = rough[6:len(rough)]
        chten = bot.get_channel('362888848323117061')
        wten = bot.get_channel('360561583409201162')
        if((len(chten.voice_members)+len(wten.voice_members))>=10):
            laundo = server.get_member('73654252970446848')
            if(laundo.voice.voice_channel != chten):
                await bot.move_member(laundo, chten)
            spaces = 10 - len(chten.voice_members)
            if(spaces > 0):
                lucky = sample(wten.voice_members, spaces)
                for player in lucky:
                    await bot.move_member(player, chten)
            if(len(pw)>1):
                msg = "Heres the ten-man password: **"  + pw + "**\nJoin Up! :eggplant:"
                for vm in chten.voice_members:
                    await bot.send_message(vm, msg, tts=False)
        else:
            msg = "You don't even have ten players **fuccboi!** :eggplant:"
            await bot.send_message(ctx.message.author, msg, tts=False)

bot.run('token')
