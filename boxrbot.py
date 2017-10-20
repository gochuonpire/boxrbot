import discord
from discord.ext import commands
import random
import asyncio
import passworder
import string
import sqlite3

description = '''A bot for the boxr discord'''
bot = commands.Bot(command_prefix='.', description=description)

server_address = ("ip", port)

conn = sqlite3.connect('boxrbot.db')

getgoingpw = "333"
searching = False

def checkperms(ctx):
    allowed = ctx.message.author.id == '73654252970446848' or ctx.message.author.id == '73637559799910400' or ctx.message.author.id == '284232617363111936'
    return allowed

async def password():
    chten = bot.get_channel('362888848323117061')
    pw = passworder.getpw()
    for player in chten.voice_members:
        msg = "Click this link to join the 10 man!\nsteam://connect/" + server_address[0] + ":" + str(server_address[1]) + "/" + pw
        msg2 = "\nOr copy&paste this into your console: connect " + server_address[0] + ":" + str(server_address[1]) + ";password " + pw
        msg += msg2
        await bot.send_message(player, msg)
    return pw;

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    newGame = discord.Game(name="message me .help", url="https://i.imgur.com/n4qxP6L.png")
    await bot.change_presence(game=newGame)

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
    else:
        if searching and after.id == '73654252970446848':
            if ch.id != '362888848323117061' and ch.id != '360561583409201162' and ch.id != '360561642506813440' and ch.id != '360561674752622609':
                searching = False
        if bch != None:
            if ch.id == '362888848323117061' and searching and bch.id != '362888848323117061':
                msg = "Click this link to join the 10 man!\nsteam://connect/" + server_address[0] + ":" + str(server_address[1]) + "/" + getgoingpw
                msg2 = "\nOr copy&paste this into your console: connect " + server_address[0] + ":" + str(server_address[1]) + ";password " + getgoingpw
                msg += msg2
                await bot.send_message(after, msg)
            elif ch.id == '360561583409201162' and searching:
                await bot.move_member(after, chten)
        else:
            if ch.id == '362888848323117061' and searching:
                msg = "Click this link to join the 10 man!\nsteam://connect/" + server_address[0] + ":" + str(server_address[1]) + "/" + getgoingpw
                msg2 = "\nOr copy&paste this into your console: connect " + server_address[0] + ":" + str(server_address[1]) + ";password " + getgoingpw
                msg += msg2
                await bot.send_message(after, msg)
            elif ch.id == '360561583409201162' and searching:
                await bot.move_member(after, chten)
    if len(chten.voice_members) == 10 and searching:
        print("No longer waiting for players")
        seraching = False

@bot.command(pass_context=True)
async def subscribe(ctx):
    """Adds you to the updatelist"""
    if ctx.message.channel.is_private == True:
        c = conn.cursor()
        t = (ctx.message.author.id,)
        c.execute('SELECT * FROM subscribers WHERE user=?', t)
        result = c.fetchone()
        if result !=None:
            if result[1]:
                msg = "You are already subscribed to streaming notifications!:thumbsup:\nTo remove yourself from this list, type .unsubscribe!"
                await bot.send_message(ctx.message.author, msg)
            else:
                upuser = (ctx.message.author.id, True)
                c.execute('REPLACE INTO subscribers (user, subscribed) values (?, ?)', upuser)
                msg = "You have been added to the notification list. We will notify you when launders is live!:thumbsup:\nTo remove yourself from this list, type .unsubscribe!"
                await bot.send_message(ctx.message.author, msg)
        else:
            newuser = (ctx.message.author.id, True)
            c.execute('INSERT INTO subscribers (user, subscribed) values (?, ?)', newuser)
            msg = "You have been added to the notification list. We will notify you when launders is live!:thumbsup:\nTo remove yourself from this list, type .unsubscribe!"
            await bot.send_message(ctx.message.author, msg)
        conn.commit()

@bot.command(pass_context=True)
async def unsubscribe(ctx):
    """Removes you from the updatelist"""
    if ctx.message.channel.is_private == True:
        c = conn.cursor()
        t = (ctx.message.author.id,)
        c.execute('SELECT * FROM subscribers WHERE user=?', t)
        result = c.fetchone()
        if result !=None:
            if result[1]:
                upuser = (ctx.message.author.id, False)
                c.execute('REPLACE INTO subscribers (user, subscribed) values (?, ?)', upuser)
                msg = "You have been removed from the update list. We will no longer notify you when launders is live!"
                await bot.send_message(ctx.message.author, msg)
                conn.commit()
            else:
                msg = "You already aren't subscribed to streaming notifications!\nTo receive notifications, type .subscribe!"
                await bot.send_message(ctx.message.author, msg)
        else:
            msg = "You already aren't subscribed to streaming notifications!\nTo receive notifications, type .subscribe!"
            await bot.send_message(ctx.message.author, msg)

@bot.command(pass_context=True, name="password")
async def pw(ctx):
    """Sends the given password to the users in the 10man voice channel"""
    if ctx.message.channel.is_private == True:
        if(checkperms(ctx)):
            vc = bot.get_channel('362888848323117061')
            for vm in vc.voice_members:
                if(vm.id != ctx.message.author.id):
                    rough = ctx.message.content
                    pw = rough[10:len(rough)]
                    msg = "Heres the ten-man password: **"  + pw + "**\nJoin Up! :eggplant:"
                    await bot.send_message(vm, msg)
                else:
                    rough = ctx.message.content
                    pw = rough[10:len(rough)]
                    msg = "Password **" + pw + "** sent successfully :thumbsup:"
                    await bot.send_message(vm, msg)

@bot.command(pass_context=True)
async def tenman(ctx):
    """Changes the password to the server and sends the new one to players"""
    global searching
    global getgoingpw
    if ctx.message.channel.is_private == True:
        server = bot.get_server('106386168593010688')
        if checkperms(ctx):
            chten = bot.get_channel('362888848323117061')
            wten = bot.get_channel('360561583409201162')
            if((len(chten.voice_members)+len(wten.voice_members))>=10):
                try:
                    laundo = server.get_member('73654252970446848')
                    if(laundo.voice.voice_channel != chten):
                        await bot.move_member(laundo, chten)
                except AttributeError:
                    msg = "A tenman without launders? Haha yeah fuck that guy."
                    await bot.send_message(ctx.message.author, msg)
                spaces = 10 - len(chten.voice_members)
                if(spaces > 0):
                    print("Staring tenman with " + str(spaces) + " extra spots")
                    lucky = sample(wten.voice_members, spaces)
                    for player in lucky:
                        print("Moving " + player.name)
                        await bot.move_member(player, chten)
                else:
                    print("Starting tenman with no extra spots")
                await password()
            else:
                for player in wten.voice_members:
                    print("Moving " + player.name)
                    await bot.move_member(player, chten)
                print("Starting tenman with " + str(len(chten.voice_members)) + " extra spots")
                print("Waiting for new members")
                getgoingpw = await password()
                searching = True

@bot.command(pass_context=True, category="ten-man")
async def stoptenman(ctx):
    """Stop automatically filling your ten man / sending passwords"""
    global searching
    if ctx.message.channel.is_private == True:
        searching = False
        msg = "People will no longer be bumped to 10man channel or sent password automatically"
        await bot.send_message(ctx.message.author, msg)

@bot.command(pass_context=True)
async def groupadd(ctx):
    """Gives the specified user access to your channel"""
    if ctx.message.channel.is_private == True:
        server = bot.get_server('106386168593010688')
        t = (ctx.message.author.id,)
        c = conn.cursor()
        c.execute('SELECT * FROM private WHERE owner=?', t)
        result = c.fetchone()
        if result != None:
            owner = result[0]
            if owner == ctx.message.author.id:
                rough = ctx.message.content
                user = rough[10:len(rough)]
                member = server.get_member_named(user)
                overwrite = discord.PermissionOverwrite()
                overwrite.connect = True
                overwrite.speak = True
                channel = bot.get_channel(result[1])
                await bot.edit_channel_permissions(channel, target=member, overwrite=overwrite)
                msg = member.mention + " was given access to " + channel.mention
                await bot.send_message(ctx.message.author, msg)
            else:
                await bot.send_message(ctx.message.author, "Fuck off :eggplant:")
        else:
            await bot.send_message(ctx.message.author, "Fuck off :eggplant:")
        conn.commit()

@bot.command(pass_context=True)
async def groupremove(ctx):
    """Revokes the specified user's access to your channel"""
    if ctx.message.channel.is_private == True:
        server = bot.get_server('106386168593010688')
        t = (ctx.message.author.id,)
        c = conn.cursor()
        c.execute('SELECT * FROM private WHERE owner=?', t)
        result = c.fetchone()
        if result != None:
            owner = result[0]
            if owner == ctx.message.author.id:
                rough = ctx.message.content
                user = rough[13:len(rough)]
                member = server.get_member_named(user)
                overwrite = discord.PermissionOverwrite()
                overwrite.connect = False
                overwrite.speak = False
                channel = bot.get_channel(result[1])
                await bot.edit_channel_permissions(channel, target=member, overwrite=overwrite)
                msg = member.mention + "no longer has access to " + channel.mention
                await bot.send_message(ctx.message.author, msg)
            else:
                await bot.send_message(ctx.message.author, "Fuck off :eggplant:")
        else:
            await bot.send_message(ctx.message.author, "Fuck off :eggplant:")
        conn.commit()

@bot.command(pass_context=True, hidden=True)
async def groupcreate(ctx):
    """Creates a group for the specified owner"""
    if ctx.message.channel.is_private == True:
        if(checkperms(ctx)):
            rough = ctx.message.content
            user = rough[13:len(rough)]
            server = bot.get_server('106386168593010688')
            ouser = server.get_member_named(user)
            c = conn.cursor()
            t = (ouser.id,)
            c.execute('SELECT * FROM private WHERE owner=?', t)
            result = c.fetchone()
            if result != None:
                member = server.get_member_named(user)
                if member !=None:
                    await bot.send_message(ctx.message.author, "User " + member.mention + " already has a private channel")
                else:
                    await bot.send_message(ctx.message.author, "User " + user + " already has a private channel")
            else:
                member = server.get_member_named(user)
                if member != None:
                    newch = await bot.create_channel(server, member.name + "'s Room", category='363510895982149633', type=discord.ChannelType.voice)
                    await bot.move_channel(newch, 0)
                    overwrite = discord.PermissionOverwrite()
                    overwrite.connect = True
                    overwrite.speak = True
                    overwrite.manage_channels = True
                    await bot.edit_channel_permissions(newch, target=member, overwrite=overwrite)
                    everyone_perms = discord.PermissionOverwrite()
                    everyone_perms.connect = False
                    everyone_perms.speak = False
                    await bot.edit_channel_permissions(newch, server.default_role, everyone_perms)
                    t = (member.id, newch.id)
                    c.execute("INSERT INTO private (owner, channel) values (?, ?)", t)
                    msg = "Created channel " + newch.mention + " for " + member.mention
                    await bot.send_message(ctx.message.author, msg)
                    helpmsg = "You've been assigned a private voice channel! This channel is all yours, to give you a space where you and your friends can hangout with no intrusions or interruptions. Only people you put on your guest list can join and adding people is pretty simple.\nThe three commands you can use to manage your private channel are **.groupadd .groupremove & .grouplist**. All these commands are used just by sending them to me, BOXR Bot. Just send me your friends ID (You can find this by clicking their profile wherever you see it in Discord. It should look something like this :point_right::skin-tone-3:  **Friend#4813**) with the **.groupadd** command and I'll add them to the guest list of your private channel! You can list all the people allowed in your channel by by typing **.grouplist** and remove them by typing **.groupremove Friend#4813**.\nIf you ever forget these commands, you can send me **.help** to get some assistance."
                    await bot.send_message(member, helpmsg)
            conn.commit()

@bot.command(pass_context=True, hidden=True)
async def groupdelete(ctx):
    """Deletes the group of the specified owner"""
    if ctx.message.channel.is_private == True:
        if(checkperms(ctx)):
            rough = ctx.message.content
            user = rough[13:len(rough)]
            server = bot.get_server('106386168593010688')
            ouser = server.get_member_named(user)
            c = conn.cursor()
            t = (ouser.id,)
            c.execute('SELECT * FROM private WHERE owner=?', t)
            result = c.fetchone()
            if result != None:
                owner = server.get_member(result[0])
                channel = bot.get_channel(result[1])
                c.execute('DELETE FROM private WHERE owner=?', t)
                msg = "Deleted channel " + channel.mention + " for " + owner.mention
                await bot.send_message(ctx.message.author, msg)
                bot_perms = discord.PermissionOverwrite()
                bot_perms.connect = True
                bot_perms.speak = True
                for smem in server.members:
                    if smem.id == '362978129301471234':
                        await bot.edit_channel_permissions(channel, smem, overwrite=bot_perms)
                await bot.delete_channel(channel)
                conn.commit()
            else:
                msg = "Channel not found for " + ouser.mention
                await bot.send_message(ctx.message.author, msg)

@bot.command(pass_context=True)
async def grouplist(ctx):
    """Lists all the people that can access your channel"""
    if ctx.message.channel.is_private == True:
        c = conn.cursor()
        t = (ctx.message.author.id,)
        c.execute('SELECT * FROM private WHERE owner=?', t)
        result = c.fetchone()
        if result != None:
            channel = bot.get_channel(result[1])
            lines = []
            for mov in channel.overwrites:
                if mov[0] is not discord.Role:
                    if mov[1].connect:
                        msg = mov[0].mention + " :white_check_mark:"
                        lines.append(msg)
                    else:
                        msg = mov[0].mention + " :x:"
                        lines.append(msg)
            msg = ""
            for line in lines[1:]:
                line += "\n"
                msg += line
            await bot.send_message(ctx.message.author, msg)
        else:
            msg = "Channel not found for " + ctx.message.author.mention
            await bot.send_message(ctx.message.author, msg)

bot.run('token')
