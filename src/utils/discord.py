import discord
from discord.ext import commands
from src.utils.utils import getFromEnv
from src.utils.log import addLog

def launchBot():
    token = getFromEnv('DISCORD_TOKEN')

    intents = discord.Intents.default()
    client = commands.Bot(command_prefix="/", intents=intents)

    @client.event
    async def on_ready():
        addLog(f"Bot {client.user} is ready")

        activity = discord.Activity(type=discord.ActivityType.watching, name="Charts")
        await client.change_presence(status=discord.Status.online, activity=activity)

    client.run(token)
