from discord.ext import commands
import json

class DefaultCommands(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def hi(self, ctx):
        await ctx.send(f'Hi {ctx.author}!')

    @commands.command()
    async def setprefix(self, ctx, *, newprefix: str):
        with open('serverprefixes.json', 'r') as file:
            prefix = json.load(file)
    
        prefix[str(ctx.guild.id)] = newprefix

        with open('serverprefixes.json', 'w') as file:
            json.dump(prefix, file, indent=4)

async def setup(client):
    await client.add_cog(DefaultCommands(client))
