import discord
import time
import asyncio

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style

import wolframalpha_api, openweather_api, mapquest_api
import wikipedia

style.use("fivethirtyeight")
client = discord.Client()

def community_report(guild):
    '''
        Tracks the server's users and their online status to monitor overall health of the server.
    '''
    online = 0
    idle = 0
    offline = 0

    for gm in guild.members:
        if str(gm.status) == "online":
            online += 1
        elif str(gm.status) == "idle":
            idle += 1 
        else:
            offline += 1
    
    return online, idle, offline

def removeKeyWord(message, keyword):
    '''
        This method edits input text. For example, if you send the message "wolfram calories in bread" or "calories in
        bread wolfram", the progrma will recognize "wolfram" and call this function to change the text to "calroies in
        brea" which will then be sent to wolfram. 
    '''
    if str(message).endswith(keyword):
        message = message[:-len(keyword)].strip()
    elif str(message).startswith(keyword):
        message = message[len(keyword):].strip()
        
    return str(message)

async def user_metrics_background():
    '''
        A scheduled task that tracks various statistics from the server and save the data to a graph every 30 seconds.
    '''
    await client.wait_until_ready()

    # create a reference to your Discord server-guild
    global brb_guild
    brb_guild = client.get_guild("client_id")

    while not client.is_closed():
        try:
            online, idle, offline = community_report(brb_guild)
            with open("user_metrics.csv", "a") as f:
                f.write(f"{int(time.time())}, {online}, {idle}, {offline}\n")

            plt.clf()

            df = pd.read_csv("user_metrics.csv", names = ["time", "online", "idle", "offline"])
            df["date"] = pd.to_datetime(df["time"], unit = "s")
            df["total"] = df["online"] + df["idle"] + df["offline"]
            df.drop("time", 1, inplace = True)
            df.set_index("date", inplace = True)

            print(df.head())
            df["online"].plot()

            plt.legend()
            plt.savefig("user_status.png")

            await asyncio.sleep(30)

        except Exception as e:
            print(str(e))
            await asyncio.sleep(30)

@client.event
async def on_ready():
    '''
        This event is expected by the client, runs once when the bot is connected to the 
        server, and outputs a notification of login.
    '''
    print(f"We successfully logged in as {client.user}")

@client.event
async def on_message(message):
    '''
        This event happens per any message and responds to messages matching specific criteria.
    '''
    print(f"{message.channel} : {message.author} : {message.author.name}")

    if "bunrieubot.logout()" == message.content:
        await client.close()
    
    elif "Hello BRB" == message.content:
        await message.channel.send(f"Good day to you {message.author.name}")

    elif "bunrieubot.member_count()" == message.content:
        await message.channel.send(f"```py\n{brb_guild.member_count}```")

    elif "bunrieubot.community_report()" == message.content:
        online, idle, offline = community_report(brb_guild)
        await message.channel.send(f"```py\nOnline: {online} \nIdle: {idle} \nOffline: {offline}```")
        
        graph_file = discord.File("user_status.png", filename = "user_status.png")
        await message.channel.send("user_status.png", file = graph_file)

    elif "bunrieubot.wiki()" in message.content:
        edit_message = removeKeyWord(message.content, "bunrieubot.wiki()")
        print(edit_message)
        try:
            await message.channel.send(wikipedia.summary(edit_message)[0:1500] + "...")
        except:
            await message.channel.send("Request was NOT found using Wikipedia. Please be more specific.")

    elif "bunrieubot.weather()" in message.content:
        edit_message = removeKeyWord(message.content, "bunrieubot.weather()")
        try:
            data = openweather_api.fetchWeatherData(edit_message)
            await message.channel.send(openweather_api.outputWeatherData(data))
        except:
            await message.channel.send("There was an Open Weather Map Error. Please try again.")

    elif "bunrieubot.wolfram()" in message.content:
        edit_message = removeKeyWord(message.content, "bunrieubot.wolfram()")
        try:
            data = wolframalpha_api.fetchWolframData(edit_message)
            await message.channel.send(wolframalpha_api.outputWolframData(data))
        except:
            await message.channel.send("Request was NOT found using Wolfram Alpha. Please be more specific.")

    elif "bunrieubot.mapquest()" in message.content:
        edit_message = removeKeyWord(message.content, "bunrieubot.mapquest()")
        try:
            data = mapquest_api.fetchMapData(edit_message)
            await message.channel.send(mapquest_api.outputMapData(data))
        except:
            await message.channel.send("There was a MapQuest Error. Please try again.")

client.loop.create_task(user_metrics_background())
client.run("bot_token")

# For more information, proceed to the Discord API Documentation at https://discordpy.readthedocs.io/en/rewrite/api.html .
#                                      Discord Developer Portal at https://discordapp.com/developers/applications/ .