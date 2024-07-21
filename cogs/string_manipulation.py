from discord.ext import commands
import json
import re

class StringManipulation(commands.Cog):
    with open('data/lazer_dictionary.json') as file:
        lazer_dictionary = json.load(file)

    def __init__(self, client):
        self.client = client
    
    def lazerify(arg: str):
        arg = re.sub(r'(?<![\s|^])ing|(?<![\s|^])in', 'an', arg.lower().strip()) # might look weird when diphthongs are considered 
        arg = re.sub(r'ph', r'f', arg)
        for word, lazer_word in StringManipulation.lazer_dictionary.items():
            arg = arg.replace(word.lower(), lazer_word)
        return arg

    @commands.command()
    async def shout(self, ctx, *, content : str):
        await ctx.send(content.upper())

    @commands.command()
    async def reverse(self, ctx, *, content):
        await ctx.send(content[::-1])

    @commands.command()
    async def lazerify(self, ctx, *, content:lazerify):
        await ctx.send(content)

async def setup(client):
    await client.add_cog(StringManipulation(client))
