import os
from simple_chalk import chalk, green
import discord
from dotenv import load_dotenv
from function.loader import nocache
from lib.message import msgHandler
load_dotenv()


if __name__ == "__main__":
    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True

    bot_name = os.getenv("BOT_NAME")
    bot = discord.Client(intents=intents)
    # bot = commands.Bot(command_prefix='!', description='', intents=intents)

    @bot.event
    async def on_ready():
        print(f'Logged in as {bot.user} (ID: {bot.user.id})')
        await bot.change_presence(activity=discord.Activity(
            type=discord.ActivityType.playing, name="Silent treatment"))
        print(f'{green.yellow("[SYS]")} {bot_name} is now online!')
        print(
            f'{green.cyan("[DEV]")} {green.magenta("Welcome back, Owner! Hope you are doing well :3")}')

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return

        await msgHandler(bot, message)

    bot.run(os.getenv('DC_TOKEN'))
