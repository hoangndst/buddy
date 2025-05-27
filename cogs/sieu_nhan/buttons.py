import discord
from cogs.common_buttons import ReturnToMenuButton
from cogs.sieu_nhan.api import get_random_superhero, create_superhero_embed

class SuperheroButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label='Superheroes', 
            style=discord.ButtonStyle.primary, 
            custom_id='superhero_button',
            emoji='🦸‍♂️'
        )

    async def callback(self, interaction: discord.Interaction):
        # Show loading embed first
        loading_embed = discord.Embed(
            title="🦸‍♂️ Loading Superhero...",
            description="Fetching a random superhero for you! ⚡",
            color=0xffa500
        )
        loading_embed.set_footer(text="⏳ Please wait...")
        
        loading_view = discord.ui.View(timeout=None)
        loading_view.add_item(ReturnToMenuButton(custom_id="return_to_menu_from_superhero_loading"))
        
        await interaction.response.edit_message(content=None, embed=loading_embed, view=loading_view)
        
        try:
            # Fetch superhero data
            superhero_data = await get_random_superhero()
            embed = create_superhero_embed(superhero_data)
            view = SuperheroView()
            
            await interaction.followup.edit_message(
                interaction.message.id,
                content=None,
                embed=embed,
                view=view
            )
            
        except Exception as error:
            error_embed = discord.Embed(
                title="❌ Superhero Error",
                description="Something went wrong while fetching superhero data.",
                color=0xff0000
            )
            error_embed.add_field(
                name="Error Details",
                value=f"```{str(error)[:100]}...```" if len(str(error)) > 100 else f"```{str(error)}```",
                inline=False
            )
            error_embed.add_field(
                name="What you can do:",
                value="• Try again in a moment\n• Check your internet connection\n• Return to main menu",
                inline=False
            )
            error_embed.set_footer(text="🔄 Please try again")
            
            error_view = discord.ui.View(timeout=None)
            error_view.add_item(ReturnToMenuButton(custom_id="return_to_menu_from_superhero_error"))
            
            await interaction.followup.edit_message(
                interaction.message.id,
                content=None,
                embed=error_embed,
                view=error_view
            )

class GetAnotherHeroButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label='Get Another Hero', 
            style=discord.ButtonStyle.success, 
            custom_id='get_another_hero_button',
            emoji='🎲'
        )

    async def callback(self, interaction: discord.Interaction):
        # Show loading state
        loading_embed = discord.Embed(
            title="🦸‍♂️ Getting Another Hero...",
            description="Fetching a new random superhero! ⚡",
            color=0xffa500
        )
        loading_embed.set_footer(text="⏳ Please wait...")
        
        await interaction.response.edit_message(embed=loading_embed, view=None)
        
        try:
            # Fetch new superhero data
            superhero_data = await get_random_superhero()
            embed = create_superhero_embed(superhero_data)
            view = SuperheroView()
            
            await interaction.followup.edit_message(
                interaction.message.id,
                content=None,
                embed=embed,
                view=view
            )
            
        except Exception as error:
            error_embed = discord.Embed(
                title="❌ Error Getting New Hero",
                description="Something went wrong while fetching a new superhero.",
                color=0xff0000
            )
            error_embed.add_field(
                name="What you can do:",
                value="• Try again\n• Return to main menu",
                inline=False
            )
            
            error_view = discord.ui.View(timeout=None)
            error_view.add_item(GetAnotherHeroButton())
            error_view.add_item(ReturnToMenuButton(custom_id="return_to_menu_from_superhero_error2"))
            
            await interaction.followup.edit_message(
                interaction.message.id,
                content=None,
                embed=error_embed,
                view=error_view
            )

class SuperheroView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(GetAnotherHeroButton())
        self.add_item(ReturnToMenuButton(custom_id="return_to_menu_from_superhero"))
