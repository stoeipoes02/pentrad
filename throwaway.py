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