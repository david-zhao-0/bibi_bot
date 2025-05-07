from discord.ext import commands
from discord import MessageType
import random
import os
import sys
import json

class DefaultCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['reset'])
    @commands.has_guild_permissions(manage_channels=True)
    async def restart(self, ctx):
        await ctx.send("Restarting bot...")
        os.execv(sys.executable, ['python'] + sys.argv)

    @commands.command(aliases=['hello', 'sup', 'yo'])
    async def hi(self, ctx):
        await ctx.send(f'Hi {ctx.author}!')

    @commands.command()
    @commands.has_guild_permissions(manage_messages=True)
    async def setprefix(self, ctx, *, newprefix: str):
        with open('data/serverprefixes.json', 'r') as file:
            prefix = json.load(file)
    
        prefix[str(ctx.guild.id)] = newprefix

        with open('data/serverprefixes.json', 'w') as file:
            json.dump(prefix, file, indent=4)

        await ctx.send(f'Prefix successfully set to \"{newprefix}\"')

    @commands.command()
    async def roll(self, ctx, n_dice = 1):
        def roll_n_dice(n):
            sum = 0
            for _ in range(n):
                sum = sum + random.randint(1,6)
            return sum
        if n_dice > 0 and n_dice < 1e6:
            await ctx.send(f'{ctx.author} rolled a **{roll_n_dice(n_dice)}** with {n_dice} dice')
        else:
            await ctx.send(f'Cannot roll {n_dice} dice!')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(f'Welcome {member.mention}!')

async def setup(client):
    await client.add_cog(DefaultCommands(client))
