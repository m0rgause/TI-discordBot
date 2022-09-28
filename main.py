import os
from simple_chalk import chalk, green
import discord
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import CommandNotFound
from dotenv import load_dotenv
from function.loader import nocache
from lib.message import msgHandler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
load_dotenv()


class Bot(BotBase):
    def __init__(self):
        self.prefix = os.getenv("PREFFIX")
        self.bot_name = os.getenv("BOT_NAME")
        self.ready = False
        self.guild = None
        self.owner_id = [521850751543148563]
        self.token = os.getenv("DC_TOKEN")
        self.scheduler = AsyncIOScheduler()
        super().__init__(
            command_prefix=self.prefix,
            owner_ids=self.owner_id,
            intents=discord.Intents.all())

    def run(self, version):
        self.VERSION = version
        print(f'{green.yellow("[SYS]")} Running Bot....')
        super().run(self.token, reconnect=True)

    async def on_connect(self):
        print(f'{green.yellow("[SYS]")} Bot Connected')

    async def on_disconnect(self):
        print(f'{green.yellow("[SYS]")} Bot Disconnected')

    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("Something went wrong.")
        raise

    async def on_command_error(self, ctx, exc):
        if isinstance(exc, CommandNotFound):
            await ctx.send("Invalid command used.")
        elif hasattr(exc, "original"):
            raise exc.original
        else:
            raise exc

    async def on_ready(self):
        if not self.ready:
            self.ready = True
            # print(f'Logged in as {self.user} (ID: {self.user.id})')
            await self.change_presence(activity=discord.Activity(
                type=discord.ActivityType.playing, name="Silent treatment"))
            print(f'{green.yellow("[SYS]")} {self.bot_name} is now online!')
            print(
                f'{green.cyan("[DEV]")} {green.magenta("Welcome back, Owner! Hope you are doing well :3")}')
        else:
            print(f'{green.yellow("[SYS]")} {self.bot_name} Reconnected!')

    async def on_message(self, message):
        if message.author == self.user:
            return

        await msgHandler(self, message)


bot = Bot()
bot.run("0.0.1")
