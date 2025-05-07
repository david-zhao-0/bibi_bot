from discord.ext import commands
from discord import Embed
from json import JSONDecodeError
import json
import requests
import random

SAFEBOORU_BASE_LINK = "https://safebooru.org/index.php?page=dapi&s=post&q=index&limit=1000&json=1&tags="
DEFAULT_AMOUNT = 3

class ImageBoards(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def safebooru(self, ctx, *, message):
        tags = message.split(" ")
        amount = DEFAULT_AMOUNT
        amount_specified = True
        
        try:
            amount = int(tags[len(tags) - 1])
        except ValueError:
            amount_specified = False
            await ctx.send("No amount specified. 3 images will be retrieved.")
        
        if amount > 10:
            await ctx.send("You can't request more than 10 images at a time!")
        else:
            link =  SAFEBOORU_BASE_LINK + "+".join(tags[:-1]) if amount_specified else SAFEBOORU_BASE_LINK + "+".join(tags)
            
            response = requests.get(link)
            html = response.text
            embeds = []

            try:

                json_output = json.loads(html)
                random_indices = random.sample(list(range(0, len(json_output))), k=amount)

                for idx in random_indices:

                    embed = Embed(type="image")
                    current_entry = json_output[idx]

                    embed.set_image(url=current_entry['file_url'])
                    source_link = current_entry['source'] if current_entry['source'] else "No source found."
                    embed.add_field(name="Source", value=source_link)
                    embeds.append(embed)

                await ctx.send(f"{len(json_output)} posts found with the tags {tags}. Selecting {amount} at random.")
                await ctx.send(embeds=embeds)
            except JSONDecodeError:
                await ctx.send(f"No results found for tag(s): {tags}!")
            except IndexError:
                await ctx.send(f"Not enough images to send: {len(embed)} images found for {tags}")

async def setup(client):
    await client.add_cog(ImageBoards(client))