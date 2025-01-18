# Local imports 
from src.algo import algo
from src.discord import DiscordBot
from src.log import initLog, displayError

# External imports
import asyncio

async def main(): 
    initLog()

    discord_bot = DiscordBot()
    _ = asyncio.create_task(discord_bot.start())
    await discord_bot.wait_until_ready()

    try:
        while True:
            await algo(discord_bot)
            await asyncio.sleep(60)

    except Exception as e:
        displayError(e)

if __name__ == "__main__":
    asyncio.run(main())