import discord
from discord.ext import commands
from discord import Member
from discord.ext.commands import has_permissions, BotMissingPermissions
import json
import requests
import asyncio
import pandas as pd
import csv

# importing credentials
from apikeys import *

intents = discord.Intents.all()
intents.members = True

client = commands.Bot(command_prefix = '!', intents=intents)


# bot ready message and status
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.dnd, activity=discord.Streaming(name='minecraft',url='https://twitch.tv/'))
    print("Bot is ready")


# simple test command
@client.command()
async def hello(ctx):
    await ctx.send("hello i am bot")



# dad joke
@client.command()
async def joke(ctx):

    url = "https://dad-jokes.p.rapidapi.com/random/joke"

    headers = {
        "X-RapidAPI-Key": JOKEAPIKEY,
        "X-RapidAPI-Host": "dad-jokes.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers)
    await ctx.send(json.loads(response.text)['body'][0]['setup'])
    await asyncio.sleep(3)
    await ctx.send(json.loads(response.text)['body'][0]['punchline'])




# member join/remove/update
@client.event
async def on_member_join(member):
    channel = client.get_channel(1012764403537543238)
    await channel.send(f"welcome {member}")

@client.event
async def on_member_remove(member):
    channel = client.get_channel(1012764403537543238)
    await channel.send(f"goodbye {member}")

@client.event
async def on_member_update(before, after):
    channel = client.get_channel(1012764403537543238)
    await channel.send(f'it used to be: {before.nick}')
    await channel.send(f'it is now: {after.name}')
    
    


### voice
@client.command(pass_context = True)
async def join(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("Not in a voice channel")

@client.command(pass_context = True)
async def leave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send('i left the voice channel')
    else:
        await ctx.send('not in a voice dummy')


### kick
@client.command()
@has_permissions(kick_members=True)
async def kick(ctx, member: Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'user {member} has been kicked')

### ban
@client.command()
@has_permissions(ban_members=True)
async def ban(ctx, member: Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'user {member} has been banned')


# embed
@client.command()
async def embed(ctx):

    embed = discord.Embed(title='Dog', url='https://google.com', description='we love dog', color=0x4dff4d)
    embed.set_author(name=ctx.author.name, url='https://www.instagram.com/kick_buur/',icon_url=ctx.author.avatar)
    embed.set_thumbnail(url='https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/Sunset_2007-1.jpg/800px-Sunset_2007-1.jpg')
    embed.add_field(name='currency', value=10, inline=True)
    embed.add_field(name='items', value='potion', inline=True)
    embed.set_footer(text='bye')

    await ctx.channel.send(embed=embed)






# private message to user
@client.command()
async def message(ctx, user:discord.Member, *, message=None):
    message = f'hey there {ctx.author} wants to say hello'
    await user.send(message)



# error exceptions sucha as missingpermissions and unknown commands
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("No permission to run this command")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("Above command doesn't exist")






@client.command()
async def all_stats(ctx):
    data = pd.read_csv('game.csv')
    embed = discord.Embed(title='Stats', url='https://google.com', description='All Stats', color=0x4dff4d)

    for index, row in data.iterrows():
        embed.add_field(name=row['name'], value=f"Health: {row['health']}\nAttack: {row['attack']}\nGold: {row['gold']}", inline=True)

    await ctx.send(embed=embed)



@client.command()
async def solo_stats(ctx, name='kick'):
    data = pd.read_csv('game.csv')
    row = data.loc[data['name'] == name]

    # Check if the row exists
    if not row.empty:
        # Get the stats from the row
        health = row.iloc[0]['health']
        attack = row.iloc[0]['attack']
        gold = row.iloc[0]['gold']
        # Create the embed with the stats
        embed = discord.Embed(title=name, description=f"Health: {health}\nAttack: {attack}\nGold: {gold}", color=discord.Color.blue())
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"No stats found for {name}")


@client.command()
async def change_stats(ctx, name):
    with open('game.csv', mode='r') as game:
        game_reader = csv.DictReader(game)
        rows = list(game_reader)
    
    found = False
    for row in rows:
        if row['name'] == name:
            row['gold'] = str(int(row['gold']) + 10)
            found = True
    
    if found:
        with open('game.csv', mode='w', newline='') as game:
            fieldnames = ['name', 'health', 'attack', 'gold']
            game_writer = csv.DictWriter(game, fieldnames=fieldnames)
            game_writer.writeheader()
            game_writer.writerows(rows)
        await ctx.send(f"{name} now has 10 more gold!")
    else:
        await ctx.send(f"{name} not found in the game.")






# --- TO-DO-list ---
# 1. buttons
# 2. graph
# 3. tradingbot
# 4. 



client.run(TOKEN)
