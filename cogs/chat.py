from discord.ext import commands
from google import genai
from google.genai import types
import os

MAX_CHAR_LENGTH = 2000

class Chat(commands.Cog):

    gemini_client = genai.Client(api_key=os.environ["GEMINI_KEY"])
    chat = gemini_client.chats.create(model="gemini-2.0-flash")

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def chat(self, ctx, *, prompt):
        response = self.gemini_client.models.generate_content(
            model="gemini-2.0-flash",
            config=types.GenerateContentConfig(
                max_output_tokens=3000,
                temperature=1.0,
                system_instruction="You are a Japanese housecat. Your name is Bibi."
            ),
            contents=prompt
        )
        if len(response.text) < MAX_CHAR_LENGTH:
            await ctx.send(response.text)
            return
        else:
            messages = []

            start = 0
            end = MAX_CHAR_LENGTH
            while start < len(response.text):
                message_fragment = response.text[start:end]
                start = end
                end += MAX_CHAR_LENGTH
                messages.append(message_fragment)
            
            for message_fragment in messages:
                await ctx.send(message_fragment)

async def setup(client):
    await client.add_cog(Chat(client))
