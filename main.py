import discord
from discord.ext import commands
#from discord import Member
#from discord.ext.commands import has_permissions, MissingPermissions
import json
import requests
import asyncio
import pandas as pd
import csv
import os
from PIL import Image
#from io import BytesIO
from time import time
import aiofiles


# importing own external libraries
from bektest import discordbacktest
from oscillators import uniquespotcoins, getdataasgraph, hotcoins, entryprice

# importing credentials
from pentrad.apikeys import *





'''
Issues:
1. backtest | link to backtest graph is not present and no server hosts it :(
2. backtest | url for image is static image
3. backtest | embed doenst show color of winning/losing backtest (color is static green)
4. creative with help | https://gist.github.com/matthewzring/9f7bbfd102003963f9be7dbcf7d40e51 
5. graph | interval D, W and M not implemented
'''


# ---------------DISCORD BOT SETUP-----------------------#

intents = discord.Intents.all()
intents.members = True

client = commands.Bot(command_prefix = '!', intents=intents)

# bot ready message and status
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.dnd, activity=discord.Streaming(name='Minecraft Legends',url='https://twitch.tv/'))
    print("Bot is ready")



@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command likely doesn't exist. :(")


@client.command()
async def prefix(ctx, new_prefix):
    """Allows users to change the command prefix."""
    client.command_prefix = new_prefix
    await ctx.send(f"The command prefix has been changed to {new_prefix}")


@client.event
async def on_guild_join(guild):
    """Create a new folder when the bot joins a new server."""
    # Get the ID of the new server
    server_id = guild.id
    # Create a new folder for the server if it doesn't already exist
    if not os.path.exists(f"pentrad/servers/{server_id}"):
        os.makedirs(f"pentrad/servers/{server_id}")


client.remove_command('help') # Remove the default help command
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




# -----------------ACTUAL CODE------------------------#

@client.command()
async def allcoins(ctx):
    allsymbolcoins = uniquespotcoins()

    array_string = str(allsymbolcoins)

    embed = discord.Embed(color=0x00ff00)
    embed.add_field(name="All available coins: ", value=array_string)

    await ctx.send(embed=embed)
    
@client.command()
async def coin(ctx, *args):
    try:

        if not args: # check if args is empty
            args = ('BTC', 'ETH', 'DOGE', 'XRP') # set default value
        coindetails = hotcoins(*args)

        for i in coindetails:
            embed = discord.Embed(title=i['symbol'])
            embed.add_field(name='Price', value=i['lastPrice'], inline=True)
            embed.add_field(name='24H High', value=i['highPrice24h'], inline=True)
            embed.add_field(name='24H Low', value=i['lowPrice24h'], inline=True)
            embed.add_field(name='Volume', value=i['volume24h'], inline=True)

            await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send("something went wrong")

@client.command()
async def setup(ctx):


    username = ctx.author.name
    tag = ctx.author.discriminator
    user_id = ctx.author.id
    server_id = ctx.guild.id
    money = 100

    beginpath = f"pentrad/servers/{server_id}/"
    userspath = f"{beginpath}users.csv"
    tradespath = f"{beginpath}trades.csv"




    user_exists = False
    if os.path.exists(userspath):
        with open(userspath, "r", newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == str(user_id):
                    user_exists = True
                    await ctx.send('user already exists')
                    break

    if not user_exists:
        if os.path.exists(userspath):
            with open(userspath, "a", newline='') as file:
                writer = csv.writer(file)
                writer.writerow([user_id, username, tag, money]) 
        else:
            with open(userspath, "w", newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["user_id", "username", "tag", "money"])
                writer.writerow([user_id, username, tag, money])
        
        await ctx.send('account created')




    if not os.path.exists(tradespath):
        if not os.path.exists(tradespath):
            with open(tradespath, "w", newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["user_id", "timestamp", "symbol", "side", "entryprice", "leverage", "money", "takeprofit", "stoploss"])



color_mapping = {
    (0, 100, 'Iron'): discord.Color(int("0x3B3B3B", 16)),
    (100, 200, 'Bronze'): discord.Color(int("0xA5855E", 16)),
    (200, 300, 'Silver'): discord.Color(int("0xCDD3D1", 16)),
    (300, 400, 'Gold'): discord.Color(int("0xEFD862", 16)),
    (400, 500, 'Platinum'): discord.Color(int("0x3AA1B3", 16)),
    (500, 600, 'Diamond'): discord.Color(int("0xA872EE", 16)),
    (600, 700, 'Ascendant'): discord.Color(int("0x389366", 16)),
    (700, float('inf'), 'Immortal'): discord.Color(int("0xB7376F", 16))
}


@client.command()
async def account(ctx, var=None):

    if var is None:
        user_id = str(ctx.author.id)
    else:
        user_id = var[2:-1]

    server_id = ctx.guild.id
    # Open the CSV file
    with open(f'pentrad/servers/{server_id}/users.csv', 'r') as file:
        # Create a CSV reader object
        reader = csv.reader(file)

        # Skip the header row
        next(reader)

        # Loop through the rows and create a message string
        user_found = False
        for row in reader:
            if row[0] == user_id:
                user_found = True
                break


       # guild = ctx.guild
        # Send the message to Discord
        if user_found:
            user = client.get_user(int(user_id))
            money = int(row[3])

            color = discord.Color.light_grey()
            for key, value in color_mapping.items():
                if key[0] <= money < key[1]:
                    color = value
                    rank = key[2]

                    break


            embed = discord.Embed(title="Account Info", color=color)
            embed.add_field(name="Username", value=row[1])
            embed.add_field(name="Money", value=row[3])
            embed.add_field(name="winrate", value="placeholder")
            embed.add_field(name="rank", value = rank)
            embed.set_thumbnail(url=user.avatar)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"No user with ID {user_id} found.")




@client.command(aliases=['emo'])
async def upload_emojis(ctx):
    # Get the guild object

    # Loop through each color and create an image
    if not os.path.exists("pentrad/colors/0-100.png"):
        for color_range, color_code in color_mapping.items():
            # Convert discord.Color to RGB tuple
            color_tuple = color_code.to_rgb()

            # Create a new image with the desired color
            image = Image.new("RGB", (25, 25), color_tuple)

            # Define the file path for the image
            file_name = f"{color_range[0]}-{color_range[1]}.png"
            file_path = os.path.join("pentrad/colors", file_name)

            # Save the image to a file
            image.save(file_path)




    guild = ctx.guild
    # Loop through the color mapping and upload each emoji
    for color_range, color_code in color_mapping.items():
        file_name = f"{color_range[0]}-{color_range[1]}"
        file_path = f"pentrad/colors/{file_name}.png"

        # Read the binary data of the image file
        with open(file_path, "rb") as f:
            emoji_image = f.read()

        # Create the emoji name
        emoji_name = file_name.replace("-", "_")

        # Check if the emoji already exists
        emoji = discord.utils.get(guild.emojis, name=emoji_name)

        if emoji is not None:
            await ctx.send(f"Emoji {emoji_name} already exists")
            continue

        try:
            # Upload the emoji to the server
            emoji = await guild.create_custom_emoji(name=emoji_name, image=emoji_image)
            await ctx.send(f"Created emoji: {emoji.name}")
        except Exception as e:
            await ctx.send(f"Failed to create emoji: {e}")




@client.command(aliases=['rank'])
async def rankings(ctx):
    try:
        server_id = ctx.guild.id
        guild = ctx.guild
        # Read CSV file
        with open(f'pentrad/servers/{server_id}/users.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            user_list = list(reader)

        # Sort users by their money value
        user_list.sort(key=lambda x: int(x['money']), reverse=True)

        # Create embed
        embed = discord.Embed(title='Trader Rankings', color=discord.Color.blurple())

        # Loop through color ranges
        for start, end, name in color_mapping:
            # Categorize users in this range
            users = []
            for user in user_list:
                money = int(user['money'])
                if start <= money < end:
                    users.append(user)

            # Create field value
            field_value = ''
            for user in users:
                field_value += f"{user['username']} - ${user['money']}\n"

            # Add field to embed
            emoji_name = f"{start}_{end}.png"
            emoji = discord.utils.get(guild.emojis, name=emoji_name.split(".")[0])
            if emoji:
                embed.add_field(name=f"{name} {start}-{end} {emoji}", value=field_value, inline=False)
            else:
                embed.add_field(name=f"{name} {start}-{end}", value=field_value, inline=False)

        await ctx.send(embed=embed)

    except Exception as e:
        print(e)



class SimpleView(discord.ui.View):
    def __init__(self, author, guild, **kwargs):
        super().__init__(**kwargs)
        self.author_id = author.id
        self.guild_id = guild.id

    async def disable_all_items(self):
        for item in self.children:
            item.disabled = True
        await self.message.edit(view=self)

    async def on_timeout(self) -> None:
        await self.disable_all_items()

    @discord.ui.button(label="Long", style=discord.ButtonStyle.success)
    async def buybutton(self, interaction: discord.Interaction, button: discord.ui.button):
        if interaction.user.id == self.author_id:
            embed = discord.Embed(title='Recommended buy', description='buying bitcoin', color=0x00ff00)

            await interaction.response.send_message(embed=embed)

        self.stop()

    @discord.ui.button(label="Short", style=discord.ButtonStyle.red)
    async def sellbutton(self, interaction: discord.Interaction, button: discord.ui.button):
        if interaction.user.id == self.author_id:
            embed = discord.Embed(title='Recommended buy', description='selling bitcoin', color=0xff0000)

            with open(f'pentrad/servers/{self.guild_id}/users.csv', 'r') as file:
                reader = csv.reader(file)
                
                user_found = False
                for row in reader:
                    if row[0] == str(self.author_id):
                        total_margin = row[3]
                        user_found = True
                        break

            embed.add_field(name='total money', value=total_margin)
            embed.add_field(name='half of money', value=int(total_margin)/2)

            
            await interaction.response.send_message(embed=embed)
            
        self.stop()





@client.command(aliases=["price", "current"],
            description="Will display a graph of the chosen coin, ***timeframe*** and candles.\n **Example:** !graph *BTC* 15 20 classic False\n Check https://testnet.bybit.com/  for all the available coins.\n Interval is limited to: 1 3 5 15 30 60 120 240 360 720 D M W.\n Candles has a range from 1 - 200.\n Styles are classic, charles, mike, blueskies, starsandstripes, brasil and yahoo.\n Volume is True or False")
async def graph(ctx, symbol="BTC", interval=15, candles=10, style="yahoo", volume=True):
    """Displays a chart of your chosen coin"""
    try:
        intervallist = [1,3,5,15,30,60,120,240,360,720]
        if interval not in intervallist:
            await ctx.send(f"Please use intervals of {intervallist}.")
            raise Exception

        if candles not in range(1, 201):
            await ctx.send("Please choose x candles between the range 1 - 200.")
            raise Exception
        
        styleslist = ['classic', 'charles', 'mike', 'blueskies', 'starsandstripes', 'brasil', 'yahoo']
        if style not in styleslist:
            await ctx.send(f"Please choose a style of {styleslist}.")
            raise Exception
        

        newsymbol = symbol
        symbol = f'{symbol}USDT'
        graphname = getdataasgraph(symbol, interval, candles, style, volume)
        url = f'http://213.73.188.84:8080/{graphname}'
        embed = discord.Embed(title=f"{newsymbol} Graph", color=0x808080)
        embed.set_author(name=ctx.author.name, url='https://www.instagram.com/kick_buur/',icon_url=ctx.author.avatar)
        embed.add_field(name='Interval', value=interval)
        embed.add_field(name='Candles', value=candles)
        embed.add_field(name='Style', value=style)
        embed.add_field(name='Volume', value=volume)

        embed.set_image(url=url)


        await ctx.channel.send(embed=embed)
        view = SimpleView(author=ctx.author, guild=ctx.guild, timeout=10)
        message = await ctx.send(view=view)
        view.message = message
        await view.wait()
        # await view.disable_all_items()

    except Exception as e:
        # Log the error
        print(f"Error: {e}")
        await ctx.channel.send("Sorry, there was an error while sending the graph. It could be that the coin you are requesting doesn't exist. Otherwise feel free to message discord user Kick#6476 about your error.")





@client.command(aliases=['open', 'buy'])
async def opentrade(ctx, symbol="BTC", leverage=1, side="buy", takeprofit=None, stoploss=None):
    try:
        async with aiofiles.open(f'pentrad/servers/{ctx.guild.id}/users.csv', 'r') as file:
            contents = await file.read()

        reader = csv.reader(contents.splitlines())

        for row in reader:
            if row[0] == str(ctx.author.id):
                money = row[3]
                break

        user_id = ctx.author.id
        timestamp = round(time())
        entry = entryprice(symbol)

        async with aiofiles.open(f'pentrad/servers/{ctx.guild.id}/trades.csv', mode='r') as file:
            contents = await file.read()
            reader = csv.reader(contents.splitlines())
            for row in reader:
                if len(row) >= 7 and row[0] == str(user_id) and row[2] == symbol:
                    await ctx.send(f"You already have an open trade on {symbol}.")
                    return

        async with aiofiles.open(f'pentrad/servers/{ctx.guild.id}/trades.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            markprice = float(entryprice(symbol))


            if leverage not in range(1, 101):
                await ctx.send("Please use a leverage between 1 and 100")
                raise Exception

            if side != "buy" and side != "sell":
                await ctx.send("Please only use 'buy' or 'sell' for a side")
                raise Exception



            if side == "buy":
                if takeprofit is None:
                    takeprofit = 10_000_000.0
                if stoploss is None:
                    stoploss = 0.0
            elif side == "sell":
                if takeprofit is None:
                    takeprofit = 0.0
                if stoploss is None:
                    stoploss = 10_000_000.0


            if (side == "buy" and (markprice > takeprofit or markprice < stoploss)):
                await ctx.send(f"wrong {side}")
                raise Exception
            if (side == "sell" and (markprice < takeprofit or markprice > stoploss)):
                await ctx.send(f"wrong")
                raise Exception
            
            await writer.writerow([user_id, timestamp, symbol, side, entry, leverage, money, takeprofit, stoploss])

        await ctx.send(f"Successfully opened a {side} trade on {symbol} with {leverage}x leverage.")
    
    except Exception as e:
        await ctx.send(e)



@client.command(aliases=['close','sell'])
async def closetrade(ctx, symbol="BTC"):
    try:
        markprice = float(entryprice(symbol))

        with open(f'pentrad/servers/{ctx.guild.id}/trades.csv') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['user_id'] == str(ctx.author.id) and row['symbol'] == symbol:
                    side = row['side']
                    leverage = row['leverage']
                    money = float(row['money'])
                    entry = float(row['entryprice'])

                    if side == "buy":
                        profit = (money*int(leverage) / entry) * markprice
                    elif side == "sell":
                        profit = abs((money*int(leverage) / entry) * markprice)

                    await ctx.send(f"Profit for {symbol} trade: {float(profit) - float(leverage)*float(money)}")

                    break  # Exit the loop once we find the matching trade

            else:
                await ctx.send("No trades found for this user and symbol")

    except Exception as e:
        await ctx.send(e)








# see open positions
# select position through









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




# @client.command(aliases=["pos", "p"], description="lists all open positions")
# async def position(ctx, symbol="BTCUSDT"):
#     open  = oscillators.get_open_positions(symbol)
#     if open['retCode'] != 0:
#         raise Exception(open)
#     else:
#         data = open['result']['list'][0]

#         unrealisedPnl = data['unrealisedPnl']
#         side = data['side']
#         entryPrice = data['entryPrice']
#         markPrice = data['markPrice']
#         leverage = data['leverage']
#         takeProfit = data['takeProfit']
#         stopLoss = data['stopLoss']
#         trailingStop = data['trailingStop']
#         liqPrice = data['liqPrice']
#         occClosingFee = float(data['occClosingFee'])
#         positionValue = float(data['positionValue'])


#         embed = discord.Embed(title=f"coin:***{symbol}*** side:***{side}***", color = 0x00ff00 if float(unrealisedPnl) >= 0 else 0xff0000)
#         embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)
#         embed.add_field(name='profit/loss', value=f"```{unrealisedPnl}```", inline=False)

#         embed.add_field(name='entry price', value=entryPrice, inline=True)
#         embed.add_field(name='mark price', value=markPrice, inline=True)

#         embed.add_field(name='leverage', value=leverage, inline=False)

#         embed.add_field(name='takeProfit', value=takeProfit, inline=True)
#         embed.add_field(name='stopLoss', value=stopLoss, inline=True)
#         embed.add_field(name='trailingStop', value=trailingStop, inline=True)
#         embed.add_field(name='liqPrice', value=liqPrice, inline=True)

#         embed.add_field(name='closingFee', value=round(occClosingFee, 2), inline=True)
#         embed.add_field(name='positionValue', value=round(positionValue, 2), inline=True)

#         view = SimpleView(timeout=6)
#         message = await ctx.send(embed=embed, view=view)
#         view.message = message

#         await view.wait()
#         await view.disable_all_items


# @client.command(aliases=["place", "order"], description="place an order of symbol, buy, ordertype, qty, price\n Example: !place_order BTCUSDT Buy Limit 0.01 10000")
# async def place_order(ctx, symbol="BTCUSDT", side="Buy", orderType="Limit", qty="0.01", price="10000"):
#     order = oscillators.create_order(symbol="BTCUSDT", side="Buy", orderType="Limit", qty="0.01", price="10000")
#     await ctx.send(order)






# @client.command(aliases=["losses", "wins", "trades", "history"], description="Will display your profits and losses.")
# async def winrate(ctx):
#     profitloss = oscillators.PnL(symbol="BTCUSDT")



#     negative = []
#     positive = []

#     for items in profitloss['result']['list']:
#         item = items['closedPnl']
#         if float(item) <= 0:
#             negative.append(item)
#         else:
#             positive.append(item)        

#     await ctx.send(positive)



# private message to user
@client.command()
async def message(ctx, user:discord.Member, *, message=None):
    message = f'hey there {ctx.author} wants to say hello'
    await user.send(message)




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
