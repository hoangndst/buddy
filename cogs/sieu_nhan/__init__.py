from discord.ext import commands
from .api import get_random_superhero, create_superhero_embed


class SuperheroCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="superhero", aliases=["hero", "sieu_nhan"])
    async def random_superhero(self, ctx):
        """Get a random superhero image."""
        # Show loading message
        loading_msg = await ctx.send("🦸‍♂️ Fetching a random superhero for you... ⚡")

        try:
            # Fetch superhero data
            superhero_data = await get_random_superhero()
            embed = create_superhero_embed(superhero_data)

            # Edit the loading message with the result
            await loading_msg.edit(content=None, embed=embed)

        except Exception as error:
            await loading_msg.edit(content=f"❌ Error fetching superhero: {str(error)}")


async def setup(bot):
    await bot.add_cog(SuperheroCog(bot))
