import os
from dotenv import load_dotenv
load_dotenv()


async def msgHandler(bot, message):
    try:
        channel = message.channel
        author = message.author
        guild = message.guild
        content = message.content
        prefix = os.getenv("PREFIX")

        print(channel, author, guild, content)

    except:
        print(f"[ERROR]")
