import sys
import os
from twitchio.ext import commands

class GlarbokBot(commands.Bot):

    BOK_NATION_MSG = (
        "lnrShrok lnrBok lnrShrok lnrShrok lnrBok lnrShrok "
        "lnrShrok lnrBok lnrShrok lnrShrok lnrBok lnrShrok "
        "lnrShrok lnrBok lnrShrok lnrShrok lnrBok lnrShrok "
        "BOK NATION  lnrShrok lnrBok lnrShrok lnrShrok lnrBok "
        "lnrShrok lnrShrok lnrBok lnrShrok lnrShrok lnrBok "
        "lnrShrok lnrShrok lnrBok lnrShrok lnrShrok lnrBok lnrShrok"
    )

    BOK_WALL_MSG = (
        "lnrBok lnrBok lnrBok lnrShrok lnrBok lnrBok lnrBok lnrShrok "
        "lnrBok lnrBok lnrBok lnrShrok BOK WALL lnrShrok "
        "lnrBok lnrBok lnrBok lnrShrok lnrBok lnrBok lnrBok lnrShrok "
        "lnrBok lnrBok lnrBok lnrShrok"
    )

    def __init__(self, streak_target):
        super().__init__(
            token=os.getenv("TWITCH_TOKEN"),
            prefix='!',
            initial_channels=['LateNightRetro']
        )
        self.streak_count = 0
        self.streak_target = streak_target

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        print(f'Streak target set to {self.streak_target}.')

    async def event_message(self, message):
        if message.echo:
            return

        content = message.content.lower()
        if "bok nation" in content:
            await message.channel.send(self.BOK_NATION_MSG)
            return

        if message.author.name.lower() == "glarbok":
            self.streak_count += 1
            if self.streak_count >= self.streak_target:
                await message.channel.send(self.BOK_WALL_MSG)
                self.streak_count = 0
        else:
            self.streak_count = 0

        await self.handle_commands(message)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python bokbot.py <streak_target>")
        sys.exit(1)

    try:
        streak_target = int(sys.argv[1])
    except ValueError:
        print("Error: streak_target must be an integer.")
        sys.exit(1)

    bot = GlarbokBot(streak_target)
    bot.run()