from discord.ext import commands
import re

class StringManipulation(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    def lazerify(arg: str):
        lazer_dictionary = {
            "ate" : "8",
            "just" : "juh",
            "pterodactyl" : "teradatool",
            "your" : "yo",
            "i haven't" : "ian",
            "even" : "een",
            "shit" : "shyt",
            "i'm" : "um",
            "supposed" : "pose",
            "little" : "li",
            " the " : " da ",
            " to " : " ta ",
            " don't" : "on",
            " than " : " dan ",
            " then " : " den ",
            " that " : " dat ",
            "what" : "wat",
            "wouldn't" : "woodan",
            "i ain't" : "ain",
            "you" : "yu",
            "tomorrow" : "tmr",
            "bitch" : "bih",
            "wigging" : "wigan",
            "everytime" : "err tyme",
            "like" : "lyke",
        }
        arg = arg.lower()
        arg = re.sub(r'(?<![\s|^])ing|(?<![\s|^])in', 'an', arg.strip()) #might look weird when dipthongs are considered 
        arg = re.sub(r'ph', r'f', arg)
        for word, lazer_word in lazer_dictionary.items():
            arg = arg.replace(word.lower(), lazer_word)
        return arg

    @commands.command()
    async def shout(self, ctx, *, content : str):
        await ctx.send(content.upper())

    @commands.command()
    async def lazerify(self, ctx, *, content:lazerify):
        await ctx.send(content)

    @commands.command()
    async def reverse(self, ctx, *, content):
        await ctx.send(content[::-1])

async def setup(client):
    await client.add_cog(StringManipulation(client))
