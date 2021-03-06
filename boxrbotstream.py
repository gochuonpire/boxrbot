import discord
from discord.ext import commands
from tinydb.operations import delete
import asyncio
from twitch import TwitchClient
import sqlite3
import string

bot = discord.Client()

def r_gen(size=7, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

async def checkStream():
    try:
        server = bot.get_server('106386168593010688')
        client = TwitchClient('twitch_api_client_id')
        stream = client.streams.get_stream_by_user('twitch_channel_id')
        vc = server.get_channel('141316972750045185')
        try:
            if(stream.id is not None):
                flag = 1
                async for message in bot.logs_from(vc, 5):
                    if(message.author.id == '362978129301471234'):
                        if(len(message.embeds)>0):
                            flag = 0
                        else:
                            await bot.delete_message(message)
                if(flag == 1):
                    eMsg = discord.Embed(title=stream.channel.status, url=stream.channel.url, description="Playing: " + stream.channel.game)
                    rando = r_gen()
                    imgUrl = stream.preview["large"] + "?test=" + rando
                    eMsg.set_image(url=imgUrl)
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
                        await bot.send_message(vc, msg)
                if flag == 1:
                    msg = "launders is offline! You can message " + bot.user.mention + " with **.subscribe** for a message every time he goes live!:pager:"
                    await bot.send_message(vc, msg)
    except:
        print("Unexpected error:", sys.exc_info()[0])

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
