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
import oscillators

# importing credentials
from pentrad.apikeys import *

'''
Issues:
1. backtest | link to backtest graph is not present and no server hosts it :(
2. backtest | url for image is static image
3. backtest | embed doenst show color of winning/losing backtest (color is static green)
4. creative with help | https://gist.github.com/matthewzring/9f7bbfd102003963f9be7dbcf7d40e51 
'''


intents = discord.Intents.all()
intents.members = True

client = commands.Bot(command_prefix = '!', intents=intents)


# bot ready message and status
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.dnd, activity=discord.Streaming(name='minecraft',url='https://twitch.tv/'))
    print("Bot is ready")

client.remove_command('help') # Remove the default help command

# simple test command
@client.command()
async def hello(ctx):
    """Types a simple hello in the chat"""
    await ctx.send("hello i am bot")



@client.command(aliases=["yelp", "elp"], description="Will show you all the commands or more details about one command\n Example: !help hello")
async def help(ctx, *args):
    """Displays help about the bot's commands"""
    if not args:
        # If no command is specified, show a list of all commands and their descriptions
        embed = discord.Embed(title="Command List", description="Here's a list of all my commands and their descriptions:")
        for command in client.commands:
            embed.add_field(name=command.name, value=command.help, inline=False)
        await ctx.send(embed=embed)
    else:
        # If a command is specified, show the command's aliases and description
        for command in client.commands:
            if args[0] == command.name or args[0] in command.aliases:
                embed = discord.Embed(title=f"Command: {command.name}", description=command.description)
                if command.aliases:
                    embed.add_field(name="Aliases", value=", ".join(command.aliases), inline=False)
                await ctx.send(embed=embed)
                break
        else:
            await ctx.send("That command doesn't exist.")



# dad joke
@client.command(aliases=["funny", "jest", "humor"], description="Will tell you a funny dad joke\nExample: !joke")
async def joke(ctx):
    """Will type a funny dad joke"""

    url = "https://dad-jokes.p.rapidapi.com/random/joke"

    headers = {
        "X-RapidAPI-Key": JOKEAPIKEY,
        "X-RapidAPI-Host": "dad-jokes.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers)
    await ctx.send(json.loads(response.text)['body'][0]['setup'])
    await asyncio.sleep(5)
    await ctx.send(json.loads(response.text)['body'][0]['punchline'])


 

@client.command(aliases=["price", "current"],
            description="Will display a graph of the chosen coin, ***timeframe*** and candles.\n **Example:** !graph *BTCUSDT* 15 20 classic False\n Check https://testnet.bybit.com/  for all the available coins.\n Interval is limited to: 1 3 5 15 30 60 120 240 360 720 D M W.\n Candles has a range from 1 - 200.\n Styles are classic, charles, mike, blueskies, starsandstripes, brasil and yahoo.\n Volume is True or False")
async def graph(ctx, symbol="BTCUSDT", interval=15, candles=10, style="yahoo", volume=True):
    """Displays a chart of your chosen coin"""
    try:
        graphname = oscillators.getdataasgraph(symbol, interval, candles, style, volume)
        url = f'http://213.73.188.84:8080/{graphname}'
        embed = discord.Embed(title="graph", url='http://213.73.188.84:8080/BTCUSDTD4.png', description='graph image', color=0x4dff4d)
        embed.set_author(name=ctx.author.name, url='https://www.instagram.com/kick_buur/',icon_url=ctx.author.avatar)
        embed.set_thumbnail(url='https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/Sunset_2007-1.jpg/800px-Sunset_2007-1.jpg')
        embed.add_field(name='Current value', value='10000')
        embed.set_image(url=url)
        embed.set_footer(text="byebye")
        await ctx.channel.send(embed=embed)
    except Exception as e:
        # Log the error
        print(f"Error: {e}")
        # Send an error message to the channel
        await ctx.channel.send("Sorry, there was an error while sending the graph. It could be that the coin you are requesting doesn't exist. Otherwise feel free to message discord user Kick#6476 about your error.")




@client.command(aliases=["pos", "p"], description="lists all open positions")
async def position(ctx, symbol="BTCUSDT"):
    try:
        open  = oscillators.get_open_positions(symbol)
        if open['retCode'] != 0:
            raise Exception(open)
        else:
            data = open['result']['list'][0]

            unrealisedPnl = data['unrealisedPnl']
            side = data['side']
            entryPrice = data['entryPrice']
            markPrice = data['markPrice']
            leverage = data['leverage']
            takeProfit = data['takeProfit']
            stopLoss = data['stopLoss']
            trailingStop = data['trailingStop']
            liqPrice = data['liqPrice']
            occClosingFee = float(data['occClosingFee'])
            positionValue = float(data['positionValue'])


            embed = discord.Embed(title=f"coin:***{symbol}*** side:***{side}***", color = 0x00ff00 if float(unrealisedPnl) >= 0 else 0xff0000)
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)
            embed.add_field(name='profit/loss', value=f"```{unrealisedPnl}```", inline=False)

            embed.add_field(name='entry price', value=entryPrice, inline=True)
            embed.add_field(name='mark price', value=markPrice, inline=True)

            embed.add_field(name='leverage', value=leverage, inline=False)

            embed.add_field(name='takeProfit', value=takeProfit, inline=True)
            embed.add_field(name='stopLoss', value=stopLoss, inline=True)
            embed.add_field(name='trailingStop', value=trailingStop, inline=True)
            embed.add_field(name='liqPrice', value=liqPrice, inline=True)

            embed.add_field(name='closingFee', value=round(occClosingFee, 2), inline=True)
            embed.add_field(name='positionValue', value=round(positionValue, 2), inline=True)

            await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send("This coin doesn't exist or you are not in a position with this coin.")




@client.command(aliases=["place", "order"], description="place an order of symbol, buy, ordertype, qty, price\n Example: !place_order BTCUSDT Buy Limit 0.01 10000")
async def place_order(ctx, symbol="BTCUSDT", side="Buy", orderType="Limit", qty="0.01", price="10000"):
    order = oscillators.create_order(symbol="BTCUSDT", side="Buy", orderType="Limit", qty="0.01", price="10000")
    await ctx.send(order)






@client.command(aliases=["losses", "wins", "trades", "history"], description="Will display your profits and losses.")
async def winrate(ctx):
    profitloss = oscillators.PnL(symbol="BTCUSDT")



    negative = []
    positive = []

    for items in profitloss['result']['list']:
        item = items['closedPnl']
        if float(item) <= 0:
            negative.append(item)
        else:
            positive.append(item)        

    await ctx.send(positive)



# private message to user
@client.command()
async def message(ctx, user:discord.Member, *, message=None):
    message = f'hey there {ctx.author} wants to say hello'
    await user.send(message)

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
        with open('pentrad/game.csv', mode='w', newline='') as game:
            fieldnames = ['name', 'gold']
            game_writer = csv.DictWriter(game, fieldnames=fieldnames)
            game_writer.writeheader()
            game_writer.writerows(rows)
        await ctx.send(f"{name} now has 10 more gold!")
    else:
        await ctx.send(f"{name} not found in the game.")










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
