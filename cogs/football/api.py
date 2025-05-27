import aiohttp
import discord
from datetime import datetime, timedelta
from cogs.football.constants import LEAGUE_INFO, get_league_display_name
import os

FOOTBALL_TOKEN = os.environ.get('FOOTBALL_TOKEN')

async def get_competition_standings(competition_id):
    url = f'http://api.football-data.org/v4/competitions/{competition_id}/standings'
    headers = {
        'X-Auth-Token': FOOTBALL_TOKEN
    }
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientError as e:
            print(f"Error fetching competition standings: {e}")
            return None

async def get_competition_matches(competition_id, date_from=None, date_to=None):
    url = f'http://api.football-data.org/v4/competitions/{competition_id}/matches'
    headers = {
        'X-Auth-Token': FOOTBALL_TOKEN
    }
    
    # Set default date range if not provided (previous week to next week)
    if not date_from and not date_to:
        today = datetime.now()
        date_from = (today - timedelta(weeks=1)).strftime('%Y-%m-%d')
        date_to = (today + timedelta(weeks=1)).strftime('%Y-%m-%d')
    
    # Build query parameters
    params = {}
    if date_from:
        params['dateFrom'] = date_from
    if date_to:
        params['dateTo'] = date_to

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers, params=params) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientError as e:
            print(f"Error fetching competition matches: {e}")
            return None

def create_error_embed(league_name, error_type="standings"):
    """Create a user-friendly error embed"""
    embed = discord.Embed(
        title="⚠️ Unable to Load Data",
        description=f"Sorry, I couldn't fetch the {league_name} {error_type} right now.",
        color=0xFF0000
    )
    embed.add_field(
        name="What happened?",
        value="• The football API might be temporarily unavailable\n• There could be a network issue\n• The service might be under maintenance",
        inline=False
    )
    embed.add_field(
        name="What can you do?",
        value="• Try again in a few moments\n• Check if other leagues work\n• Contact support if the issue persists",
        inline=False
    )
    embed.set_footer(text="🔄 Please try again later")
    return embed
        
async def get_standings(competition_id):
    data = await get_competition_standings(competition_id)
    league_info = LEAGUE_INFO.get(competition_id, {})
    league_name = get_league_display_name(competition_id)
    
    if not data:
        return create_error_embed(league_name, "standings")
    
    # Create enhanced embed with league-specific colors and emoji
    emoji = league_info.get('emoji', '🏆')
    color = league_info.get('color', 0x00ff00)
    description = league_info.get('description', f"Latest standings for the {league_name}")
    
    embed = discord.Embed(
        title=f"{emoji} {league_name} - Current Standings",
        description=f"*{description}*",
        color=color
    )
    
    # Set thumbnail with fallback
    try:
        embed.set_thumbnail(url=data['competition']['emblem'])
    except (KeyError, TypeError):
        pass
    
    table = data['standings'][0]['table']

    # Enhanced standings display with more information
    if len(table) > 0:        
        position = []
        name = []
        points = []
        for team in table:
            position.append(str(team['position']))
            name.append(f'**{team["team"]["shortName"]}**')
            points.append(str(team['points']))
        
        embed.add_field(name='Position', value='\n'.join(position), inline=True)
        embed.add_field(name='Name', value='\n'.join(name), inline=True)
        embed.add_field(name='Points', value='\n'.join(points), inline=True)

    else:
        embed.add_field(
            name="No Data Available",
            value="No standings data found for this competition.",
            inline=False
        )
    return embed

async def get_matches(competition_id, date_from=None, date_to=None):
    """Get matches for a competition with enhanced formatting similar to the image"""
    data = await get_competition_matches(competition_id, date_from, date_to)
    league_info = LEAGUE_INFO.get(competition_id, {})
    league_name = get_league_display_name(competition_id)
    
    if not data:
        return create_error_embed(league_name, "matches")
    
    # Use league-specific info from LEAGUE_INFO
    emoji = league_info.get('emoji', '⚽')
    color = league_info.get('color', 0x00ff00)
    country = league_info.get('country', '')
    
    embed = discord.Embed(
        title=f"{emoji} {league_name}",
        description=f"Recent & Upcoming Matches",
        color=color
    )
    
    # Set thumbnail with fallback
    try:
        embed.set_thumbnail(url=data['competition']['emblem'])
    except (KeyError, TypeError):
        pass
    
    matches = data['matches']
    
    if not matches:
        embed.add_field(
            name="📅 No Matches Found",
            value="No matches scheduled for the selected period.\nTry checking a different date range.",
            inline=False
        )
        return embed
    
    c_time = []
    c_match = []
    c_score = []
    for match in matches:
        home_team = match['homeTeam']['shortName']
        away_team = match['awayTeam']['shortName']
        c_match.append(f'**{home_team}**\n**{away_team}**')
        
        # Format date and time
        utc_date = match['utcDate']
        if utc_date:
            try:
                match_datetime = datetime.fromisoformat(utc_date.replace('Z', '+00:00'))
                date_str = match_datetime.strftime('%d/%m')
                time_str = match_datetime.strftime('%H:%M')
            except:
                date_str = 'TBD'
                time_str = ''
        else:
            date_str = 'TBD'
            time_str = ''
        c_time.append(f'{date_str}\n{time_str}')
        
        status = match['status']
        if status == 'FINISHED':
            c_score.append(f'{str(match["score"]["fullTime"]["home"])}\n{str(match["score"]["fullTime"]["away"])}')
        else:
            c_score.append(f'{status}\n')
            
    embed.add_field(name='Time', value='\n\n'.join(c_time), inline=True)
    embed.add_field(name='Match', value='\n\n'.join(c_match), inline=True)
    embed.add_field(name='Score', value='\n\n'.join(c_score), inline=True)
    return embed 