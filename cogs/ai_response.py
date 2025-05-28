from google import genai
from google.genai import types
import os
from discord.ext import commands


class AIResponse(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.gemini_client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
        self.model = os.environ.get("GEMINI_MODEL")

    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        # Check if the bot is mentioned
        if self.bot.user.mentioned_in(message):
            try:
                content_without_mention = message.content.replace(
                    f"<@{self.bot.user.id}>", ""
                ).strip()
                contents = [
                    types.Content(
                        role="user",
                        parts=[
                            types.Part.from_text(
                                text="""{}""".format(content_without_mention)
                            )
                        ],
                    ),
                ]
                generate_content_config = types.GenerateContentConfig(
                    temperature=0.7,
                    top_p=0.95,
                    top_k=64,
                    max_output_tokens=65536,
                    response_mime_type="text/plain",
                )
                response = []
                async with message.channel.typing():
                    for chunk in self.gemini_client.models.generate_content_stream(
                        model=self.model,
                        contents=contents,
                        config=generate_content_config,
                    ):
                        response.append(chunk.text)
                response = "".join(response)
                while len(response) > 2000:
                    split_index = response.rfind("\n", 0, 2000)
                    if split_index == -1:
                        split_index = 2000
                    await message.channel.send(response[:split_index])
                    response = response[split_index:]
                if response:
                    await message.channel.send(response)
            except Exception as e:
                await message.channel.send(
                    f"Thực sự xin lỗi, tôi không hiểu ý của bạn :cry:"
                )
                raise e


async def setup(bot):
    await bot.add_cog(AIResponse(bot))
