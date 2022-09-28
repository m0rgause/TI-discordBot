from discord.ext.commands import Cog
from discord.ext.commands import command
from simple_chalk import chalk, green


class Commands(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="ping")
    async def ping_command(self, ctx):
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms")

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("Commands")
            print(f'{green.yellow("[SYS]")} Ready to serve you Master')


async def setup(bot):
    await bot.add_cog(Commands(bot))
