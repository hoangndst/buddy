from discord.ext import commands


class Filter(commands.Cog):
    def __init__(self, bot, obscene_words):
        self.bot = bot
        self.obscene_words = obscene_words

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if any(word in message.content.lower() for word in self.obscene_words):
            await message.reply(
                f"{message.author.mention} nói bậy ít thôi câm cái mồm vào :face_with_symbols_over_mouth:"
            )


async def setup(bot):
    # read the bad words from a file
    obscene_words = set()
    with open("./assets/obscene_words.txt", "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith("#"):
                obscene_words.add(line.lower())
    await bot.add_cog(Filter(bot, obscene_words))
