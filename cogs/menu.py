from discord.ext import commands
import discord
from cogs.football.buttons import FootballButton
from cogs.sieu_nhan.buttons import SuperheroButton
from cogs.common_buttons import ReturnToMenuButton, ExitButton

class AIButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label='@buddy chat', 
            style=discord.ButtonStyle.secondary, 
            custom_id='ai_button',
            emoji='🤖'
        )

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🤖 @buddy chat",
            description="Chat with @buddy",
            color=0x9c27b0
        )
        embed.add_field(
            name="How to use:",
            value=f"Simply mention {interaction.client.user.mention} in any message to chat with @buddy",
            inline=False
        )
        embed.add_field(
            name="Example:",
            value=f"{interaction.client.user.mention} What's the weather like today?",
            inline=False
        )
        embed.add_field(
            name="Features:",
            value="• Natural conversation\n• Helpful answers\n• Multi-language support",
            inline=False
        )
        embed.set_footer(text="🧠 @buddy is powered by Gemini")
        
        view = AIView()
        await interaction.response.edit_message(content=None, embed=embed, view=view)
    
class HelpButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label='Help & Info', 
            style=discord.ButtonStyle.secondary, 
            custom_id='help_button',
            emoji='❓'
        )

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="❓ Help & Information",
            description="Welcome bro! Here's everything you need to know.",
            color=0xff9800
        )
        embed.add_field(
            name="🚀 Getting Started:",
            value="1. Click any button in the main menu\n2. Follow the instructions for each feature",
            inline=False
        )
        embed.add_field(
            name="💡 Tips:",
            value="• Use `$buddy` to access this menu anytime\n• Most features work with buttons - no typing needed!\n• @buddy responds to mentions",
            inline=False
        )
        embed.set_footer(text="🛠️ Made with ❤️")
        
        view = HelpView()
        await interaction.response.edit_message(content=None, embed=embed, view=view)

class AIView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(ReturnToMenuButton(custom_id="return_to_menu_from_ai"))

class HelpView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(ReturnToMenuButton(custom_id="return_to_menu_from_help"))

def create_main_menu_embed():
    """Create the main menu embed with enhanced styling"""
    embed = discord.Embed(
        title="🤖 @buddy - Main Menu",
        description="Hey bro! I'm @buddy - shout out to @danchoicloud_bot from Telegram",
        color=0x00d4aa
    )
    
    embed.set_footer(text="💡 Click any button to explore feature!")    
    return embed

class MenuView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot
        
        # Row 1: Main features
        self.add_item(FootballButton())
        self.add_item(SuperheroButton())
        self.add_item(AIButton())
        
        # Row 2: Utilities and help
        self.add_item(HelpButton())
        self.add_item(ExitButton())

class Menu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='buddy')
    async def menu(self, ctx):
        """Show the main menu with all available features."""
        embed = create_main_menu_embed()
        view = MenuView(self.bot)
        await ctx.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(Menu(bot))
