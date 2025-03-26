from discord.ext import commands

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        await ctx.send('Hello Internet Villager! Ask me anything.')

    @commands.command()
    async def fetch_data(self, ctx):
        data = await self.bot.db_pool.fetch('SELECT * FROM some_table')
        if data:
            await ctx.send(f'Data: {data}')
        else:
            await ctx.send('No data found.')

async def setup(bot):
    await bot.add_cog(General(bot))
