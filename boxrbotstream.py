import discord
from discord.ext import commands
from twitch import TwitchClient
from tinydb import TinyDB, Query
from tinydb.operations import delete
import asyncio

bot = discord.Client()

db = TinyDB('data.json')
Users = Query()

async def checkStream():
    print('Checking stream')
    client = TwitchClient('twitchAPIClientid')
    stream = client.streams.get_stream_by_user('twitchuserid')
    for server in bot.servers:
        for vc in server.channels:
            try:
                if(stream.id is not None):
                    if vc.id == '365175633103552512':
                            flag = 1;
                            async for message in bot.logs_from(vc, 500):
                                if(message.author.id == '362978129301471234'):
                                    if(len(message.embeds)>0):
                                        flag = 0;
                                        print('No update needed (streaming)')
                                    else:
                                        await bot.delete_message(message)
                            if(flag == 1):
                                eMsg = discord.Embed(title=stream.channel.status, url=stream.channel.url, description="Playing: " + stream.channel.game)
                                eMsg.set_thumbnail(url=stream.preview["large"])
                                eMsg.set_author(name="launders is live!")
                                await bot.send_message(vc, '', embed=eMsg)
                                await updateUsers(eMsg)
            except AttributeError:
                if vc.id == '365175633103552512':
                    async for message in bot.logs_from(vc, 500):
                        flag = 1;
                        if(message.author.id == '362978129301471234'):
                            if(len(message.embeds)>0):
                                await bot.delete_message(message)
                            else:
                                flag = 0;
                                print('No update needed (not streaming)')
                        if(flag == 1):
                            msg = "launders is offine! You can message " + bot.user.mention + " with **.subscribe** for a message every time he goes live!:pager:"
                            await bot.send_message(vc, msg, tts=False)

async def updateUsers(msg):
    print("Updating users")
    for item in db:
        if(item["sup"] == 1):
            for server in bot.servers:
                m = server.get_member(item["id"])
                await bot.send_message(m, '', embed=msg)
@bot.event
async def on_ready():
    while True:
        await checkStream()
        await asyncio.sleep(60)

bot.run('token')
