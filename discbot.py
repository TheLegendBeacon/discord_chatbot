import discord
from discord.ext import commands
from chatbot import AsyncPredictChatBot
import json

def load_settings():
    with open('botsettings.json', 'r') as f:
        return json.load(f.read())

async def set_settings(botyesorno, botchannels):
    with open('botsettings.json', 'w') as f:
        json.dump((botyesorno, botchannels), f)

class ItsAChatBot(commands.Bot):
    def __init__(self, owner_id: int, chatbot: AsyncPredictChatBot, command_prefix, **options):
        super().__init__(command_prefix, **options)
        self.chatbot = chatbot
        self.botyesorno, self.botchannels = load_settings()
        self.cache_bot_channels = {guild_id: self.get_channel(channel_id) for guild_id, channel_id in self.botchannels}
        self.owner = owner_id
        
    async def generate_response(self, input):
        response = await self.chatbot.generate_response(input)
        return response
    
    async def on_ready(self):
        for guild in self.guilds:
            if guild.id not in self.botyesorno.keys():
                self.botyesorno[guild.id] = False

        for guildid in self.botyesorno.keys():
            if self.botyesorno[guildid] == True:
                del self.botchannels[guildid]
            del self.botyesorno[guildid]
        
        await set_settings(self.botyesorno, self.botchannels)
    
    async def on_guild_join(self, guild):
        self.botyesorno[guild.id] = False
        await set_settings(self.botyesorno, self.botchannels)

    async def on_guild_leave(self, guild: discord.Guild):
        if self.botyesorno[guild.id] == True:
            del self.botchannels[guild.id]
        del self.botyesorno[guild.id]
        await set_settings(self.botyesorno, self.botchannels)
        
    async def on_message(self, message: discord.Message):
        if self.botyesorno[message.guild.id] == True:
            response: str = await self.generate_response(message)

            if message.guild.id not in self.cache_bot_channels.keys():
                self.cache_bot_channels[message.guild.id] = self.get_channel(self.botchannels[message.guild.id])

            channel: discord.TextChannel = self.cache_bot_channels[message.guild.id]
            await channel.send(response)