import aiohttp
import discord
from datetime import datetime, timedelta
from cogs.football.constants import LEAGUE_INFO, get_league_display_name
from tabulate import tabulate
import os

FOOTBALL_TOKEN = os.environ.get("FOOTBALL_TOKEN")


async def get_competition_standings(competition_id):
    url = f"http://api.football-data.org/v4/competitions/{competition_id}/standings"
    headers = {"X-Auth-Token": FOOTBALL_TOKEN}

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientError as e:
            print(f"Error fetching competition standings: {e}")
            return None


async def get_competition_matches(competition_id, date_from=None, date_to=None):
    url = f"http://api.football-data.org/v4/competitions/{competition_id}/matches"
    headers = {"X-Auth-Token": FOOTBALL_TOKEN}

    # Set default date range if not provided (previous week to next week)
    if not date_from and not date_to:
        today = datetime.now()
        date_from = today.strftime("%Y-%m-%d")
        date_to = (today + timedelta(weeks=1)).strftime("%Y-%m-%d")

    # Build query parameters
    params = {}
    if date_from:
        params["dateFrom"] = date_from
    if date_to:
        params["dateTo"] = date_to

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
        color=0xFF0000,
    )
    embed.add_field(
        name="What happened?",
        value="• The football API might be temporarily unavailable\n• There could be a network issue\n• The service might be under maintenance",
        inline=False,
    )
    embed.add_field(
        name="What can you do?",
        value="• Try again in a few moments\n• Check if other leagues work\n• Contact support if the issue persists",
        inline=False,
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
    emoji = league_info.get("emoji", "🏆")
    color = league_info.get("color", 0x00FF00)
    description = league_info.get(
        "description", f"Latest standings for the {league_name}"
    )

    embed = discord.Embed(
        title=f"{emoji} {league_name} - Current Standings",
        description=f"*{description}*",
        color=color,
    )

    # Set thumbnail with fallback
    try:
        embed.set_thumbnail(url=data["competition"]["emblem"])
    except (KeyError, TypeError):
        pass

    table = data["standings"][0]["table"]

    # Enhanced standings display with tabulate showing all teams across multiple fields
    if len(table) > 0:
        # Calculate how many teams we can fit per field (approximately 12-15 teams per field)
        teams_per_field = 20
        total_teams = len(table)

        # Split teams into chunks that fit within Discord's character limit
        for chunk_start in range(0, total_teams, teams_per_field):
            chunk_end = min(chunk_start + teams_per_field, total_teams)

            # Create table data for this chunk
            message_table = []

            # Only add headers for the first chunk
            if chunk_start == 0:
                message_table.append(["Pos", "Team", "Pts"])

            for i in range(chunk_start, chunk_end):
                team = table[i]
                message_table.append(
                    [
                        team["position"],
                        team["team"]["shortName"][:12],  # Truncate long team names
                        team["points"],
                    ]
                )

            # Use a compact tabulate format
            if chunk_start == 0:
                output = tabulate(message_table, headers="firstrow", tablefmt="simple")
            else:
                output = tabulate(message_table, tablefmt="simple")

            # Determine field name based on chunk
            if chunk_start == 0:
                field_name = "📊 League Table"
            else:
                field_name = ""

            embed.add_field(name=field_name, value=f"```\n{output}\n```", inline=False)

    else:
        embed.add_field(
            name="No Data Available",
            value="No standings data found for this competition.",
            inline=False,
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
    emoji = league_info.get("emoji", "⚽")
    color = league_info.get("color", 0x00FF00)
    country = league_info.get("country", "")

    embed = discord.Embed(
        title=f"{emoji} {league_name}",
        description=f"Upcoming 7 Days Matches",
        color=color,
    )

    # Set thumbnail with fallback
    try:
        embed.set_thumbnail(url=data["competition"]["emblem"])
    except (KeyError, TypeError):
        pass

    matches = data["matches"]

    if not matches:
        embed.add_field(
            name="📅 No Matches Found",
            value="No matches scheduled for the next 7 days.",
            inline=False,
        )
        return embed

    # Group matches by date for better organization
    from collections import defaultdict

    matches_by_date = defaultdict(list)

    for match in matches:
        utc_date = match["utcDate"]
        if utc_date:
            try:
                match_datetime = datetime.fromisoformat(utc_date.replace("Z", "+00:00"))
                date_key = match_datetime.strftime("%Y-%m-%d")
                date_display = match_datetime.strftime("%A, %d %B %Y")
            except:
                date_key = "TBD"
                date_display = "To Be Determined"
        else:
            date_key = "TBD"
            date_display = "To Be Determined"

        matches_by_date[date_key].append((match, date_display))

    # Sort dates
    sorted_dates = sorted(matches_by_date.keys())

    # Create a field for each date
    for date_key in sorted_dates:
        matches_for_date = matches_by_date[date_key]
        date_display = matches_for_date[0][1]  # Get display name from first match

        # Create table data for this date
        message_table = [["T", "M", "S"]]

        for match, _ in matches_for_date:
            home_team = match["homeTeam"]["tla"]
            away_team = match["awayTeam"]["tla"]

            # Format time
            utc_date = match["utcDate"]
            if utc_date:
                try:
                    match_datetime = datetime.fromisoformat(
                        utc_date.replace("Z", "+00:00")
                    )
                    time_str = match_datetime.strftime("%H:%M")
                except:
                    time_str = "TBD"
            else:
                time_str = "TBD"

            # Format score
            status = match["status"]
            if status == "FINISHED":
                c_score = f'{match["score"]["fullTime"]["home"]}\n{match["score"]["fullTime"]["away"]}'
            else:
                c_score = f"{status}\n"

            c_time = f"{time_str}\n"
            c_match = f"{home_team}\n{away_team}"

            message_table.append([c_time, c_match, c_score])

        # Use tabulate format
        output = tabulate(message_table, headers="firstrow", tablefmt="grid")

        # Use date as field name
        field_name = f"📅 {date_display}"

        embed.add_field(name=field_name, value=f"```\n{output}\n```", inline=False)
    return embed
