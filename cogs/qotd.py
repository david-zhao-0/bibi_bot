from dotenv import load_dotenv
load_dotenv()

import os
from discord.ext import tasks, commands
import datetime
from supabase import create_client

class QuestionOfTheDay(commands.Cog):
    supabase = create_client(os.environ.get('QOTD_DATA_URL'), os.environ.get('QOTD_DATA_KEY'))
    default_question_time = datetime.time(hour=12, minute=0, tzinfo=datetime.timezone.utc)

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def lastquestion(self, ctx):
        response = self.supabase.table("Questions").select("id", "question").order("created_at").eq("asked", False).eq("guild", str(ctx.guild)).limit(1).single().execute()
        print(response.data['question'])
        self.supabase.table("Questions").update({"asked" : True}).eq("id", response.data['id']).execute()
        await ctx.send(response)

    @commands.command()
    async def submitquestion(self, ctx, *, question : str):
        self.supabase.table("Questions").insert({
            "guild" : str(ctx.guild),
            "question" : question,
            "asked_by" : str(ctx.author),
            "asked" : False
        }).execute()
        await ctx.send('Your question was submitted!')

    @commands.command()
    async def removelastquestion(self, ctx):
        print('To implement')
        pass

    @commands.command()
    async def questions(self, ctx):
        response = self.supabase.table("Questions").select("question", count="exact").order("created_at").eq("asked", False).eq("guild", str(ctx.guild)).execute()
        for i in range(response.count):
            question = response.data[i]['question']
            await ctx.send(f'{i + 1}: {question}')

    @commands.command()
    async def start_qotd(self, ctx):
        await self.get_last_question.start(ctx)

    @commands.command()
    async def stop_qotd(self, ctx):
        await self.get_last_question.stop(ctx)

    @tasks.loop(time=default_question_time)
    async def get_last_question(self, ctx : commands.Context):
        question = self.supabase.table("Questions").select("question").eq("asked", False).execute()
        await ctx.send(question)

async def setup(client):
    await client.add_cog(QuestionOfTheDay(client))