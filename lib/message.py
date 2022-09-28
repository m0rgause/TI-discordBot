import os
from dotenv import load_dotenv
load_dotenv()


async def msgHandler(bot, message):
    """ Message Handler """
    try:
        channel = message.channel
        author = message.author
        guild = message.guild
        content = message.content
        prefix = os.getenv("PREFIX")

        # VALIDATOR
        print(message.type)

    except:
        print(f"[ERROR]")
