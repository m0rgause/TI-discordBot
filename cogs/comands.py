from discord.ext.commands import Cog
from simple_chalk import chalk, green


class Commands(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("Commands")
            print(f'{green.yellow("[SYS]")} Ready to serve you Master')


def setup(bot):
    bot.add_cog(Commands(bot))
