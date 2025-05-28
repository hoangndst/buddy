FOOTBALL_LEAGUES = {
    "PL": "Premier League",
    "PD": "La Liga",
    "SA": "Serie A",
    "FL1": "Ligue 1",
}

OPTION_TYPE_MATCH = "match"
OPTION_TYPE_STANDING = "standing"

# Comprehensive league information - single source of truth
LEAGUE_INFO = {
    "PL": {
        "label": "Premier League",
        "full_name": "English Premier League",
        "country": "England",
        "emoji": "🏴󠁧󠁢󠁥󠁮󠁧󠁿",
        "color": 0x3D195B,
        "description": "The most-watched football league in the world",
    },
    "PD": {
        "label": "La Liga",
        "full_name": "Spanish La Liga",
        "country": "Spain",
        "emoji": "🇪🇸",
        "color": 0xFF6B35,
        "description": "Home to Real Madrid and Barcelona",
    },
    "SA": {
        "label": "Serie A",
        "full_name": "Italian Serie A",
        "country": "Italy",
        "emoji": "🇮🇹",
        "color": 0x005DAA,
        "description": "Italy's premier football competition",
    },
    "FL1": {
        "label": "Ligue 1",
        "full_name": "French Ligue 1",
        "country": "France",
        "emoji": "🇫🇷",
        "color": 0x1E3A8A,
        "description": "France's top professional football league",
    },
}


def get_league_options():
    """Generate dropdown options from LEAGUE_INFO"""
    return [
        {"label": info["label"], "value": league_id, "description": info["description"]}
        for league_id, info in LEAGUE_INFO.items()
    ]


def get_league_display_name(league_id):
    """Get the display name for a league"""
    return LEAGUE_INFO.get(league_id, {}).get(
        "full_name", FOOTBALL_LEAGUES.get(league_id, "Unknown League")
    )


# Generate options dynamically from LEAGUE_INFO
FOOTBALL_LEAGUES_OPTIONS = get_league_options()
