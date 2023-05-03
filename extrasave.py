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