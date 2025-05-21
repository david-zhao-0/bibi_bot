from discord.ext import commands
from discord import HTTPException
from discord import Embed
from datetime import timedelta
import requests
import urllib.parse

TRACE_MOE_BASE_LINK = "https://api.trace.moe/search?anilistInfo&cutBorders&url={}"
SIMILARITY_CUTOFF = 0.80

class Anime(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def trace(self, ctx):

        reference_msg = None
        attached_media = None

        try:

            if ctx.message.reference:
                message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            else:
                await ctx.send("Please reply to an image, gif, or video to use this command.")
                return

            if len(message.attachments) > 0:
                attached_media = message.attachments[0]
            else:
                reference_msg = message.content

        except HTTPException as e:
            await ctx.send(e)
            return
        
        search_result = requests.get(TRACE_MOE_BASE_LINK.format(
            urllib.parse.quote_plus(
               reference_msg if not attached_media else attached_media.url
            )
        )).json()

        if search_result['error']:
            await ctx.send(search_result['error'])
            await ctx.send("Malformed media URL. Please respond to a message containing only the raw media link.")
        else:
            top_result = search_result['result'][0]
            anilist_entry = top_result['anilist']
            anime_title = anilist_entry['title']['romaji']

            embed = Embed(title=anime_title, type="rich")
            similarity_score = top_result['similarity']

            if similarity_score >= SIMILARITY_CUTOFF:
                embed.add_field(name="Similarity:", value=round(similarity_score, 4))
            else:
                await ctx.send(f"No matching scenes found with similarity score > {SIMILARITY_CUTOFF}.")
                return

            if top_result['episode']:
                embed.add_field(name="Episode:", value=f"Episode {top_result['episode']}")
                
            start_time = str(timedelta(seconds=int(top_result['from'])))
            end_time = str(timedelta(seconds=int(top_result['to'])))
            embed.add_field(name="From:", value=f"{start_time} to {end_time}")

            await ctx.send(embed=embed)

            if anilist_entry['isAdult']:
                return
            
            await ctx.send(f"[Source Video]({top_result['video']})")

async def setup(client):
    await client.add_cog(Anime(client))
