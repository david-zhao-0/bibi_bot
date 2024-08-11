from dotenv import load_dotenv
load_dotenv()

import os
import asyncio
from discord.ext import tasks, commands
import datetime
from supabase import create_client

class QuestionOfTheDay(commands.Cog):
    supabase = create_client(os.environ.get('QOTD_DATA_URL'), os.environ.get('QOTD_DATA_KEY'))
    default_question_time = datetime.time(hour=12, minute=0, tzinfo=datetime.timezone.utc)

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def lastquestion(self, ctx): #TODO -- set policies for RLS 
        response = (self.supabase.table("Questions")
                    .select("id", "question")
                    .eq("asked", True)
                    .eq("guild", str(ctx.guild))
                    .order("id", desc=True)
                    .limit(1)
                    .single()
                    .execute())
        await ctx.send('The last question that was asked: ' + response.data['question'])

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
        response = (self.supabase.table("Questions")
                    .delete()
                    .eq("asked", False)
                    .eq("guild", str(ctx.guild))
                    .eq("asked_by", str(ctx.author))
                    .limit(1)
                    .execute())
        await ctx.send(f'Your most recent QOTD question in {ctx.guild} was deleted.')

    @commands.command()
    async def nextquestions(self, ctx):
        response = (self.supabase.table("Questions")
                    .select("question", count="exact")
                    .eq("asked", False)
                    .eq("guild", str(ctx.guild))
                    .order("id")
                    .execute())
        test = "\n".join([i['question'] for i in response.data])        
        await ctx.send(f'**Upcoming questions:**\n{test}')

    @commands.command()
    async def start_qotd(self, ctx):
        await asyncio.gather(
            ctx.send(f'QOTD questions initiated in {ctx.guild} for channel {ctx.channel}.'),
            self.get_last_question.start(ctx)
        ) 
        
    @commands.command()
    async def stop_qotd(self, ctx):
        await asyncio.gather(
            ctx.send(f'QOTD questions stopped.'),
            self.get_last_question.stop(ctx)
        )

    @tasks.loop(time=default_question_time)
    async def get_last_question(self, ctx : commands.Context):
        question_to_ask = self.supabase.table("Questions").select("question").eq("asked", False).execute()
        self.supabase.table("Questions").update({"asked" : True}).eq("id", question_to_ask.data['id']).execute()
        await ctx.send(question_to_ask)

async def setup(client):
    await client.add_cog(QuestionOfTheDay(client))