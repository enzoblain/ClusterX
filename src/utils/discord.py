import asyncio
import discord
from discord.ext import commands
from src.utils.utils import getFromEnv
from src.utils.log import addLog

class DiscordBot:
    def __init__(self):
        self.token = getFromEnv('DISCORD_TOKEN')
        self.channel_id = int(getFromEnv('DISCORD_CHANNEL_ID'))

        intents = discord.Intents.default()
        intents.messages = True
        intents.guilds = True

        self.client = commands.Bot(command_prefix="/", intents=intents)
        self.channel = None
        self.ready_event = asyncio.Event()

        @self.client.event
        async def on_ready():
            addLog(f"Bot connected as {self.client.user}")
            self.channel = await self.client.fetch_channel(self.channel_id)
            self.ready_event.set()

    async def start(self):
        await self.client.start(self.token)

    async def wait_until_ready(self):
        await self.ready_event.wait()

    async def send_message(self, message):
        if self.channel is None:
            raise ValueError("Channel is not set")
        
        await self.channel.send(message)

    async def stop(self):
        await self.client.close()