import discord
from discord.ext import commands
from discbot import ItsAChatBot
from chatbot import bot
from dotenv import load_dotenv
from os import getenv

load_dotenv()
OWNER_ID = getenv('OWNER_ID')
TOKEN = getenv('TOKEN')

client = ItsAChatBot(owner_id=OWNER_ID, chatbot=bot, command_prefix='c!')

@client.command(name='enable', aliases=['setchannel', 'sc'])
async def enable(ctx, channel: discord.TextChannel):
    if client.botyesorno[ctx.guild.id] is not True:
        client.botyesorno[ctx.guild.id] = True
    client.botchannels[ctx.guild.id] = channel.id
    await ctx.send(f"Enabled chatbot in (Or switched channel to) {channel.mention}")
    
@client.command(name='disable')
async def disable(ctx):
    if client.botyesorno[ctx.guild.id] is True:
        client.botyesorno[ctx.guild.id] = False
        del client.botchannels[ctx.guild.id]
        await ctx.send("Disabled the chatbot.")
    else:
        await ctx.send("The chatbot is disabled already.")

@client.command()
async def shutdown(ctx):
    if ctx.author.id == client.owner_id:
        await ctx.send("Shutting down...")
        await client.close()
    else:
        ctx.send("No")

client.run(TOKEN)