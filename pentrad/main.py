import discord
from discord.ext import commands
from discord import Member
from discord.ext.commands import has_permissions, BotMissingPermissions
import json
import requests
import asyncio

# importing credentials
from apikeys import *

intents = discord.Intents.all()
intents.members = True

client = commands.Bot(command_prefix = '!', intents=intents)

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Streaming(name='minecraft',url='https://twitch.tv/'))
    print("Bot is ready")

@client.command()
async def hello(ctx):
    print('hey')
    await ctx.send("hello i am bot")

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


# ### kick
@client.command()
@has_permissions(kick_members=True)
async def kick(ctx, member: Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'user {member} has been kicked')


# ### ban
@client.command()
@has_permissions(ban_members=True)
async def ban(ctx, member: Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'user {member} has been banned')


@client.command()
async def embed(ctx):

    embed = discord.Embed(title='Dog', url='https://google.com', description='we love dog', color=0x4dff4d)
    embed.set_author(name=ctx.author.name, url='https://www.instagram.com/kick_buur/',icon_url=ctx.author.avatar)
    embed.set_thumbnail(url='https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/Sunset_2007-1.jpg/800px-Sunset_2007-1.jpg')
    embed.add_field(name='currency', value=10, inline=True)
    embed.add_field(name='items', value='potion', inline=True)
    embed.set_footer(text='bye')

    await ctx.channel.send(embed=embed)


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("No permission to run this command")


@client.command()
async def message(ctx, user:discord.Member, *, message=None):
    message = f'hey there {ctx.author} wants to say hello'
    await user.send(message)



client.run(TOKEN)
