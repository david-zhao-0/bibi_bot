from discord.ext import commands
from discord import Embed
import requests
from bs4 import BeautifulSoup

class ImageBoards(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def safebooru(self, ctx, *, message):
        tags = message.split(" ")
        base = "https://safebooru.org/index.php?page=post&s=list&tags="
        link = base + "+".join(tags)
        
        response = requests.get(link)
        html = response.text
        soup = BeautifulSoup(html, "html.parser")

        images = []

        image_container = soup.find_all("div", {"class":"image-list"})
        if (len(image_container) != 0):
            image_ids = []

            for child in image_container[0].children:
                if child.name == "span":
                    span_id = child.get("id")
                    image_ids.append(span_id[1:])
        
            image_url_prefix = "https://safebooru.org/index.php?page=post&s=view&id="
            source_image_links = []

            for image_id in image_ids[:5]:

                image_link = image_url_prefix + image_id
                html = requests.get(image_link).text
                soup = BeautifulSoup(html, "html.parser")
                image_container = soup.find_all("div", {"id":""})

                for child in image_container[0].children:
                    if child.name == "img":
                        source_image_link = child.get("src")
                        source_image_links.append(source_image_link)

            for image_link in source_image_links:        
                embed_image = Embed(title=message, type="image")
                embed_image.set_image(url=image_link)
                images.append(embed_image)

            for image in images:
                await ctx.send(embed=image)

        else:
            await ctx.send("No results found!")

async def setup(client):
    await client.add_cog(ImageBoards(client))