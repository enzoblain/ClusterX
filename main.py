import asyncio
from src.utils.log import initLog, displayError
from src.execution.algo import algo
from src.utils.discord import DiscordBot

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