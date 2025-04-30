from discord.ext import commands
import os
import torch
from transformers import pipeline

class Chat(commands.Cog):

    HF_TOKEN = os.environ['HF_TOKEN']

    pipeline = pipeline(
        "text-generation",
        model="meta-llama/Llama-3.2-1B",
        torch_dtype=torch.bfloat16,
        device_map="auto"
    )

    def __init__(self, client):
        self.client = client    

    @commands.command()
    async def chat(self, ctx, *, prompt : str):
        message = pipeline(prompt)
        await ctx.send(message)

async def setup(client):
    await client.add_cog(Chat(client))
