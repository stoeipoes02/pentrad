import discord
from discord.ext import commands
from discord import Member
from discord.ext.commands import has_permissions, MissingPermissions, CommandError
import json
import requests
import asyncio
import pandas as pd
import csv

# importing own external libraries
from bektest import discordbacktest
from oscillators import get_open_positions

# importing credentials
from pentrad.apikeys import *

'''
Issues:
1. backtest | link to backtest graph is not present and no server hosts it :(
2. backtest | url for image is static image
3. backtest | embed doenst show color of winning/losing backtest (color is static green)
'''





intents = discord.Intents.all()
intents.members = True

client = commands.Bot(command_prefix = '!', intents=intents)


# bot ready message and status
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.dnd, activity=discord.Streaming(name='minecraft',url='https://twitch.tv/'))
    print("Bot is ready")

@client.command(description='lists all commands')
async def commands(ctx):
    command_list = []
    for command in client.commands:
        command_list.append(command.name)
    command_list.sort()
    command_msg = "\n".join(command_list)
    await ctx.send(f'list of commands {command_msg}')



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
    await asyncio.sleep(5)
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
    if isinstance(error, CommandError):
        if isinstance(error, MissingPermissions):
            await ctx.send("You don't have permission to do that.")
        else:
            await ctx.send("An error occurred: {}".format(str(error)))






@client.command()
async def all_stats(ctx):
    data = pd.read_csv('pentrad/game.csv')
    embed = discord.Embed(title='Stats', url='https://google.com', description='All Stats', color=0x4dff4d)

    for index, row in data.iterrows():
        embed.add_field(name=row['name'], value=f"Gold: {row['gold']}", inline=True)

    await ctx.send(embed=embed)



@client.command()
async def solo_stats(ctx, name='kick'):
    data = pd.read_csv('pentrad/game.csv')
    row = data.loc[data['name'] == name]

    # Check if the row exists
    if not row.empty:
        # Get the stats from the row
        gold = row.iloc[0]['gold']
        # Create the embed with the stats
        embed = discord.Embed(title=name, description=f"Gold: {gold}", color=discord.Color.blue())
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"No stats found for {name}")


@client.command()
async def change_stats(ctx, name):
    with open('pentrad/game.csv', mode='r') as game:
        game_reader = csv.DictReader(game)
        rows = list(game_reader)
    
    found = False
    for row in rows:
        if row['name'] == name:
            row['gold'] = str(int(row['gold']) + 10)
            found = True
    
    if found:
        with open('game.csv', mode='w', newline='') as game:
            fieldnames = ['name', 'gold']
            game_writer = csv.DictWriter(game, fieldnames=fieldnames)
            game_writer.writeheader()
            game_writer.writerows(rows)
        await ctx.send(f"{name} now has 10 more gold!")
    else:
        await ctx.send(f"{name} not found in the game.")





@client.command(aliases=["pos", "p"], description="lists all open positions")
async def positions(ctx):
    open = get_open_positions()
    await ctx.send(open)


# test command for testing
# stock=GOOG, cash=10000, margin=1, commission=0, fast=12, slow=26
@client.command(aliases=['test','back','backrest', 'stock'],description='Simple Moving Average backtest')
async def backtest(ctx, stock=None, cash=10000, margin=1, commission=0, fast=12, slow=26):
    values = discordbacktest(stock, cash, margin, commission, fast, slow)
    
    embed = discord.Embed(title='SMA Backtest', url='http://127.0.0.1:8000/tests.html', description='Backtest Graph', color=0x4dff4d)
    embed.set_author(name=ctx.author.name, url='https://www.instagram.com/kick_buur/',icon_url=ctx.author.avatar)
    embed.set_thumbnail(url='https://learnpriceaction.com/wp-content/uploads/2018/05/candlestick-patterns-PDF.png')
    embed.add_field(name='profit in %', value=values['Return [%]'], inline=True)
    embed.set_footer(text='loser')


    await ctx.channel.send(embed=embed)




client.run(TOKEN)
