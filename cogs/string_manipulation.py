from discord.ext import commands
import json
import re

class StringManipulation(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def shout(self, ctx, *, content : str):
        await ctx.send(content.upper())

    @commands.command()
    async def reverse(self, ctx, *, content):
        await ctx.send(content[::-1])

async def setup(client):
    await client.add_cog(StringManipulation(client))
