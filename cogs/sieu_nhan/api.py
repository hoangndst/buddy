import aiohttp
import discord
import random
import os

SIEU_NHAN_API_BASE = os.environ.get("SIEU_NHAN_API_BASE")


async def get_random_superhero():
    """Get a random superhero image from the API"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(SIEU_NHAN_API_BASE) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    return None
    except Exception as e:
        print(f"Error fetching superhero: {e}")
        return None


def create_superhero_embed(superhero_data):
    """Create an embed for displaying superhero information"""
    if not superhero_data:
        # Fallback embed
        embed = discord.Embed(
            title="🦸‍♂️ Superhero Error",
            description="Unable to fetch superhero data at the moment. Please try again!",
            color=0xFF0000,
        )
        return embed

    # Extract data based on the API response structure
    # Adjust these fields based on what the API actually returns
    image_url = superhero_data.get(
        "image", superhero_data.get("image", superhero_data.get("image", None))
    )

    embed = discord.Embed(
        title=f"🦸‍♂️",
        color=random.choice(
            [0xFF0000, 0x00FF00, 0x0000FF, 0xFF00FF, 0xFFFF00, 0x00FFFF]
        ),
    )

    if image_url:
        embed.set_image(url=image_url)

    return embed
