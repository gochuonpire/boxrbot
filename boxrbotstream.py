import discord
from discord.ext import commands
from tinydb.operations import delete
import asyncio
from twitch import TwitchClient
import sqlite3

bot = discord.Client()

async def checkStream():
    server = bot.get_server('106386168593010688')
    client = TwitchClient('twitch_api_client_id')
    stream = client.streams.get_stream_by_user('twitch_channel_id')
    vc = server.get_channel('141316972750045185')
    try:
        if(stream.id is not None):
            flag = 1
            async for message in bot.logs_from(vc, 500):
                if(message.author.id == '362978129301471234'):
                    if(len(message.embeds)>0):
                        flag = 0
                        print('No update needed (streaming)')
                    else:
                        await bot.delete_message(message)
            if(flag == 1):
                eMsg = discord.Embed(title=stream.channel.status, url=stream.channel.url, description="Playing: " + stream.channel.game)
                eMsg.set_image(url=stream.preview["large"])
                eMsg.set_author(name="launders is live!")
                await bot.send_message(vc, '', embed=eMsg)
                await updateUsers(eMsg)

    except AttributeError:
        flag = 1
        async for message in bot.logs_from(vc, 500):
            if(message.author.id == '362978129301471234'):
                if(len(message.embeds)>0):
                    await bot.delete_message(message)
                else:
                    flag = 0
                if(flag == 1):
                    flag = 0
                    msg = "launders is offline! You can message " + bot.user.mention + " with **.subscribe** for a message every time he goes live!:pager:"
                    await bot.send_message(vc, msg, tts=False)
            if flag == 1:
                msg = "launders is offline! You can message " + bot.user.mention + " with **.subscribe** for a message every time he goes live!:pager:"
                await bot.send_message(vc, msg, tts=False)

async def updateUsers(msg):
    server = bot.get_server('106386168593010688')
    conn = sqlite3.connect('boxrbot.db')
    c = conn.cursor()
    t = (True,)
    c.execute('SELECT * FROM subscribers WHERE subscribed = ?', t)
    result = c.fetchall()
    for row in result:
        userid = row[0]
        m = server.get_member(userid)
        await bot.send_message(m, '', embed=msg)
    conn.close()

@bot.event
async def on_ready():
    while True:
        await checkStream()
        await asyncio.sleep(60)

bot.run('token')
