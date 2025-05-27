import discord
from cogs.common_buttons import ReturnToMenuButton, ExitButton
from cogs.football.constants import OPTION_TYPE_MATCH, OPTION_TYPE_STANDING, LEAGUE_INFO

def create_football_dashboard_embed():
    """Create the main football dashboard embed using LEAGUE_INFO"""
    embed = discord.Embed(
        title="⚽ Football Dashboard",
        description="Choose what you'd like to explore:",
        color=0x00ff00
    )
    embed.add_field(
        name="🏆 Standings",
        value="View current league tables and team positions",
        inline=True
    )
    embed.add_field(
        name="⚽ Matches",
        value="See recent results and upcoming fixtures",
        inline=True
    )
    
    return embed

class FootballButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label='⚽ Football', style=discord.ButtonStyle.secondary, custom_id='football_button')

    async def callback(self, interaction: discord.Interaction):
        embed = create_football_dashboard_embed()
        view = FootballOptionsView()
        await interaction.response.edit_message(content=None, embed=embed, view=view)

class FootballOptionsView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(ShowStandingButton())
        self.add_item(ShowMatchButton())
        self.add_item(ReturnToMenuButton(custom_id="return_to_menu_from_football"))
        self.add_item(ExitButton())        

class ShowMatchButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label='Show Matches', style=discord.ButtonStyle.success, custom_id='show_match_button')
        self.emoji = discord.PartialEmoji(name='⚽')

    async def callback(self, interaction: discord.Interaction):
        # Create loading embed
        loading_embed = discord.Embed(
            title="⚽ Loading Matches...",
            description="Please select a league to view recent and upcoming matches",
            color=0x00ff00
        )
        
        view = MatchLeaguesView()
        await interaction.response.edit_message(
            content=None,
            embed=loading_embed,
            view=view
        )

class ShowStandingButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label='Show Standings', style=discord.ButtonStyle.success, custom_id='show_standing_button')
        self.emoji = discord.PartialEmoji(name='📊')

    async def callback(self, interaction: discord.Interaction):
        # Create loading embed
        loading_embed = discord.Embed(
            title="🏆 Loading Standings...",
            description="Please select a league to view the current table",
            color=0x00ff00
        )
        
        view = StandingsLeaguesView()
        await interaction.response.edit_message(
            content=None,
            embed=loading_embed,
            view=view
        )

class MatchLeaguesView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        dropdown = ListLeaguesDropDown(option_type=OPTION_TYPE_MATCH)
        dropdown.custom_id = "match_leagues_dropdown"
        
        self.add_item(dropdown)
        self.add_item(ReturnToFootballOptionsButton())

class StandingsLeaguesView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        dropdown = ListLeaguesDropDown(option_type=OPTION_TYPE_STANDING)
        dropdown.custom_id = "standing_leagues_dropdown"
        
        self.add_item(dropdown)
        self.add_item(ReturnToFootballOptionsButton())

class ReturnToFootballOptionsButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label='← Back to Football', style=discord.ButtonStyle.secondary, custom_id='return_to_football_options')
    
    async def callback(self, interaction: discord.Interaction):
        embed = create_football_dashboard_embed()
        view = FootballOptionsView()
        await interaction.response.edit_message(content=None, embed=embed, view=view)

class ListLeaguesDropDown(discord.ui.Select):
    def __init__(self, option_type):
        self.option_type = option_type
        options = []
        
        for league_id, info in LEAGUE_INFO.items():
            options.append(
                discord.SelectOption(
                    label=info.get('full_name', info['label']), 
                    value=league_id, 
                    description=info['description'],
                    emoji=info['emoji']
                )
            )
        
        placeholder = '🏆 Select a league...' if option_type == OPTION_TYPE_STANDING else '⚽ Select a league...'
        super().__init__(placeholder=placeholder, min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        selected_league = interaction.data.get('values', [None])[0]
        if not selected_league:
            await interaction.response.send_message('❌ No league selected.', ephemeral=True)
            return

        # Show loading state
        loading_embed = discord.Embed(
            title="🔄 Loading...",
            description=f"Fetching {'standings' if self.option_type == OPTION_TYPE_STANDING else 'matches'} data...\nThis may take a few seconds.",
            color=0xFFFF00
        )
        loading_embed.set_footer(text="⏳ Please wait...")
        
        # Create view with back button for loading state
        loading_view = discord.ui.View(timeout=None)
        loading_view.add_item(ReturnToFootballOptionsButton())
        
        await interaction.response.edit_message(embed=loading_embed, view=loading_view)
        
        try:
            if self.option_type == OPTION_TYPE_STANDING:
                from cogs.football.api import get_standings
                result = await get_standings(selected_league)
            elif self.option_type == OPTION_TYPE_MATCH:
                from cogs.football.api import get_matches
                result = await get_matches(selected_league)
            else:
                await interaction.followup.edit_message(
                    interaction.message.id,
                    content="❌ Invalid option type",
                    embed=None,
                    view=FootballOptionsView()
                )
                return
            
            result.set_footer(text=f"Requested by {interaction.user.display_name}", icon_url=interaction.user.display_avatar.url)
            # Create enhanced view with navigation
            result_view = ResultView()
            
            await interaction.followup.edit_message(
                interaction.message.id,
                content=None,
                embed=result,
                view=result_view
            )
            
        except Exception as error:
            # Enhanced error handling
            error_embed = discord.Embed(
                title="❌ Error Loading Data",
                description=f"Something went wrong while fetching the data.",
                color=0xFF0000
            )
            error_embed.add_field(
                name="Error Details",
                value=f"```{str(error)[:100]}...```" if len(str(error)) > 100 else f"```{str(error)}```",
                inline=False
            )
            error_embed.add_field(
                name="What you can do:",
                value="• Try selecting a different league\n• Wait a moment and try again\n• Check your internet connection",
                inline=False
            )
            error_embed.set_footer(text="🔄 Please try again")
            
            error_view = discord.ui.View(timeout=None)
            error_view.add_item(ReturnToFootballOptionsButton())
            
            await interaction.followup.edit_message(
                interaction.message.id,
                content=None,
                embed=error_embed,
                view=error_view
            )

class ResultView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(ReturnToFootballOptionsButton())
