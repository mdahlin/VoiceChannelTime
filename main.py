import pickle
from os import path
from time import time

import discord

from secrets import TOKEN

pickleName = 'voiceChannelTime.pickle'

if path.exists(pickleName):
    with open(pickleName, 'rb') as handle:
        voiceChannelLog = pickle.load(handle)
else:
    voiceChannelLog = {}

voiceChannelActive = {}

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_voice_state_update(member, before, after):
    user = member.name
    if user not in voiceChannelLog:
        voiceChannelLog[user] = 0
    if before.channel is None and after.channel is not None:
        print(user + " joined")
        voiceChannelActive[user] = time()

    if after.channel is None and before.channel is not None:
        print(user + "left")
        voiceChannelLog[user] += time() - voiceChannelActive[user]
        print(voiceChannelLog)
        with open(pickleName, 'wb') as handle:
            pickle.dump(voiceChannelLog, handle, protocol=pickle.HIGHEST_PROTOCOL)

def printLeaderboard(voiceChannelLog):

    sortLog = sorted(voiceChannelLog.items(), key=lambda x: x[1], reverse=True)  

    outStr = 'Voice Channel Leaders\n----------------------\n'
    for i, user in enumerate(sortLog):
        s = '{}. {} - {} mins. \n'.format(i + 1, user[0], round(user[1]/60))
        outStr += s
    
    return outStr

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$leaderboard'):
        await message.channel.send(printLeaderboard(voiceChannelLog))

client.run(TOKEN)
