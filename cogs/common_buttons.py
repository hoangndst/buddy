import discord


class ReturnToMenuButton(discord.ui.Button):
    def __init__(self, custom_id="return_to_menu"):
        super().__init__(
            label="Return to Menu",
            style=discord.ButtonStyle.danger,
            custom_id=custom_id,
        )

    async def callback(self, interaction: discord.Interaction):
        from cogs.menu import MenuView, create_main_menu_embed

        embed = create_main_menu_embed()
        view = MenuView(interaction.client)
        await interaction.response.edit_message(content=None, embed=embed, view=view)


class ExitButton(discord.ui.Button):
    def __init__(self, custom_id="exit"):
        super().__init__(
            label="Exit", style=discord.ButtonStyle.danger, custom_id=custom_id
        )

    async def callback(self, interaction: discord.Interaction):
        content = "See ya bro! :wave:"
        await interaction.response.edit_message(
            content=content, embed=None, view=None, delete_after=5
        )
