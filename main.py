import os
from datetime import datetime
from asyncio import sleep
from glob import glob
from simple_chalk import chalk, green
import discord
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import CommandNotFound
from dotenv import load_dotenv
from function.loader import nocache
from lib.message import msgHandler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from lib.db import db

load_dotenv()

PREFIX = os.getenv("PREFFIX")
BOT_NAME = os.getenv("BOT_NAME")
OWNER_IDS = [521850751543148563]
TOKEN = os.getenv("DC_TOKEN")
COGS = [path.split("\\")[-1][:-3] for path in glob("./cogs/*.py")]


class Ready(object):
    def __init__(self):
        for cog in COGS:
            setattr(self, cog, False)

    def ready_up(self, cog):
        setattr(self, cog, True)
        print(f'{green.yellow("[SYS]")} {cog} Cog Ready')

    def all_ready(self):
        return all([getattr(self, cog) for cog in COGS])


class Bot(BotBase):
    def __init__(self):
        self.prefix = PREFIX
        self.bot_name = BOT_NAME
        self.cogs_ready = Ready()
        self.ready = False
        self.guild = None
        self.scheduler = AsyncIOScheduler()

        db.autosave(self.scheduler)
        super().__init__(
            command_prefix=self.prefix,
            owner_ids=OWNER_IDS,
            intents=discord.Intents.all())

    def setup(self):
        for cog in COGS:
            self.load_extension(f"cogs.{cog}")
            print(f'{green.yellow("[SYS]")} {cog} Cog Loaded')

    def run(self, version):
        self.VERSION = version
        print(f'{green.yellow("[SYS]")} Running Bot....')
        print(f'{green.yellow("[SYS]")} Running version {version}')
        print(f'{green.yellow("[SYS]")} Running Setup')
        self.setup()

        super().run(TOKEN, reconnect=True)

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

    # async def rules_reminder(self):
        # channel = self.get_channel()
        # await channel.send("Remember to follow the rules!")

    async def on_ready(self):
        if not self.ready:
            self.ready = True
            # self.scheduler.add_job(self.rules_reminder,CronTrigger(day_of_week=0))
            # self.scheduler.start()
            await self.change_presence(activity=discord.Activity(
                type=discord.ActivityType.playing, name="Silent treatment"))
            print(f'{green.yellow("[SYS]")} {self.bot_name} is now online!')
            print(
                f'{green.cyan("[DEV]")} {green.magenta("Welcome back, Owner! Hope you are doing well :3")}')
            while not self.cogs_ready.all_ready():
                await sleep(0.5)
        else:
            print(f'{green.yellow("[SYS]")} {self.bot_name} Reconnected!')

    async def on_message(self, message):
        if message.author == self.user:
            return

        await msgHandler(self, message)


bot = Bot()
bot.run("0.0.1")
