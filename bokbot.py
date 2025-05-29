import sys
import os
from twitchio.ext import commands
import asyncio
import random
import datetime

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

    WHERE_BOK_AT_MSG = "lnrBok lnrShrok it's {time}, where Glarbok at? lnrShrok lnrBok"

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
        self.loop.create_task(self.periodic_glarbok_check())

    async def periodic_glarbok_check(self):
        while True:
            wait_time = random.randint(1, 3 * 60 * 60)  # seconds
            await asyncio.sleep(wait_time)
            current_time = datetime.datetime.now().strftime("%-I:%M %p").lower()
            message = self.WHERE_BOK_AT_MSG.format(time=current_time)
            await self.connected_channels[0].send(message)

    async def event_message(self, message):
        if message.echo:
            return

        content = message.content.lower()
        if "bok nation" in content or "boknation" in content:
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