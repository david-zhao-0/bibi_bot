from discord.ext import commands
import requests
import urllib.parse

TRACE_MOE_BASE_LINK = "https://api.trace.moe/search?cutBorders&url={}"

class Anime(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def trace(self, ctx, *, source_file):
        search_result = requests.get(TRACE_MOE_BASE_LINK.format(
            urllib.parse.quote_plus(
                
            )
        ))