import discord
from discord.ext import commands

class ExceptionHandler(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error) -> None:

        if isinstance(error, commands.CheckFailure):
            await ctx.send("You do not have permission to use that command.")
        
        print(error)

async def setup(client):
    await client.add_cog(ExceptionHandler(client))