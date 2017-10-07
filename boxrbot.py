import discord
from discord.ext import commands
import random
import asyncio
from tinydb import TinyDB, Query
from tinydb.operations import delete
import passworder

description = '''A bot for the boxr discord'''
bot = commands.Bot(command_prefix='.', description=description)

db = TinyDB('data.json')
Users = Query()

server_address = ("ip", port)

getgoingpw = "333"
searching = False

def checkperms(ctx):
    allowed = ctx.message.author.id == '73654252970446848' or ctx.message.author.id == '73637559799910400' or ctx.message.author.id == '284232617363111936'
    return allowed

async def password():
    chten = bot.get_channel('362888848323117061')
    pw = passworder.getpw()
    for player in chten.voice_members:
        #msg = "Paste this into your console to join the 10 man!\nconnect " + server_address[0] + ":" + str(server_address[1]) + "; password " + pw
        msg = "Click this link to join the 10 man!\nsteam://connect/" + server_address[0] + ":" + str(server_address[1]) + "/" + pw
        await bot.send_message(player, msg, tts=False)
    return pw;

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.event
async def on_voice_state_update(before, after):
    global searching
    server = bot.get_server('106386168593010688')
    chten = server.get_channel('362888848323117061')
    ch = after.voice.voice_channel
    bch = before.voice.voice_channel
    if ch == None:
        if searching and after.id == '73654252970446848':
            searching = False
            print('stopping search for 10man')
    else:
        if searching and after.id == '73654252970446848':
            if ch.id != '362888848323117061' and ch.id != '360561583409201162' and ch.id != '360561642506813440' and ch.id != '360561674752622609':
                searching = False
                print('stopping search for 10man')
        if bch != None:
            if ch.id == '362888848323117061' and searching and bch.id != '362888848323117061':
                msg = "Click this link to join the 10 man!\nsteam://connect/" + server_address[0] + ":" + str(server_address[1]) + "/" + getgoingpw
                await bot.send_message(after, msg, tts=False)
            elif ch.id == '360561583409201162' and searching:
                await bot.move_member(after, chten)
        else:
            if ch.id == '362888848323117061' and searching:
                msg = "Click this link to join the 10 man!\nsteam://connect/" + server_address[0] + ":" + str(server_address[1]) + "/" + getgoingpw
                await bot.send_message(after, msg, tts=False)
            elif ch.id == '360561583409201162' and searching:
                await bot.move_member(after, chten)
    if len(chten.voice_members) == 10 and searching:
        seraching = False

@bot.command(pass_context=True)
async def stoptenman(ctx):
    """Stop automatically filling your ten man / sending passwords"""
    searching = False
    msg = "People will no longer be bumped to 10man channel or sent password automatically"
    await bot.send_message(ctx.message.author, msg, tts=False)

@bot.command(pass_context=True, name="password")
async def pw(ctx):
    """Sends the given password to the users in the 10man voice channel"""
    if(checkperms(ctx)):
        vc = bot.get_channel('362888848323117061')
        for vm in vc.voice_members:
            if(vm.id != ctx.message.author.id):
                rough = ctx.message.content
                pw = rough[10:len(rough)]
                msg = "Heres the ten-man password: **"  + pw + "**\nJoin Up! :eggplant:"
                await bot.send_message(vm, msg, tts=False)
            else:
                rough = ctx.message.content
                pw = rough[10:len(rough)]
                msg = "Password **" + pw + "** sent successfully :thumbsup:"
                await bot.send_message(vm, msg, tts=False)

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
async def tenman(ctx):
    """Changes the password to the server and sends the new one to players"""
    global searching
    global getgoingpw
    server = bot.get_server('106386168593010688')
    if checkperms(ctx):
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
            password()
        else:
            for player in wten.voice_members:
                await bot.move_member(player, chten)
            else:
                getgoingpw = await password()
                searching = True

bot.run('token')
