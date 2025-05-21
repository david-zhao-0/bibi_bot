import asyncio
import logging
from discord.ext import tasks, commands
import datetime
import sqlite3 as db
from sqlite3 import Error

DEFAULT_QUESTION_TIME = datetime.time(hour=12, minute=0, tzinfo=datetime.timezone.utc)

class QuestionOfTheDay(commands.Cog):

    question_time = DEFAULT_QUESTION_TIME

    def __init__(self, client):
        self.client = client

    def create_connection(db_file) -> db.Connection:
        conn = None
        try:
            conn = db.connect(db_file)
            return conn
        except Error as e:
            print(e)

    conn = create_connection(r"C:\Users\David\Documents\Coding\Bibi_Bot\data\questions.db")
    cursor = conn.cursor()
    
    @commands.command()
    async def lastquestion(self, ctx): 
        await ctx.send("to implement")

    @commands.command()
    async def submitquestion(self, ctx, *, question : str):
        message_data = (None, ctx.author.id, str(ctx.author), str(ctx.guild), 0, question, ctx.message.created_at.strftime('%a %d %b %Y, %I:%M%p'))
        sql =  "INSERT INTO qotd VALUES(?, ?, ?, ?, ?, ?, ?)"
        try:
            with self.conn:
                self.cursor.execute(sql, message_data)
                await ctx.send("Question submitted!")
        except Exception as e:
            await ctx.send(f"Unable to submit question: {e}")
            print(e)
        
    @commands.command()
    async def removelastquestion(self, ctx):
        sql = """
        DELETE FROM qotd WHERE question_id = (
            SELECT question_id 
            FROM qotd 
            WHERE user_id = ? AND guild = ?
            ORDER BY question_id DESC
            LIMIT 1
        )
        """
        try:
            with self.conn:
                self.cursor.execute(sql, (ctx.author.id, str(ctx.guild)))
                await ctx.send("Question removed!")
        except Exception as e:
            await ctx.send(f"Error removing entry: {e}")

    @commands.command()
    async def questions(self, ctx):
        sql = "SELECT question FROM qotd WHERE guild = ?"
        try:
            with self.conn:
                questions = self.cursor.execute(sql, (str(ctx.guild),))
                await(ctx.send("\n-".join([question[0] for question in questions.fetchall()])))
        except Exception as e:
            await ctx.send(f"Error retrieving questions: {e}")

    @commands.command()
    @commands.has_guild_permissions(manage_channels=True)
    async def start_qotd(self, ctx):
        await asyncio.gather(
            self.get_last_question.start(ctx),
            ctx.send(f"QOTD questions initiated in {ctx.guild} for channel {ctx.channel}. Questions will appear at {self.question_time.strftime('%I:%M%p')} UTC every day.")
        )
        
    @commands.command()
    @commands.has_guild_permissions(manage_channels=True)
    async def stop_qotd(self, ctx):
        self.get_last_question.cancel(),
        await ctx.send(f"QOTD stopped.")

    @tasks.loop(time=question_time)
    async def get_last_question(self, ctx):

        select_question_sql = """
            SELECT question_id, question
            FROM qotd
            WHERE guild = ? AND asked = 0
            ORDER BY question_id ASC
            LIMIT 1
        """

        update_entry_sql = "UPDATE qotd SET asked = 1 WHERE question_id = ?"

        with self.conn:
            row = self.cursor.execute(select_question_sql, (str(ctx.guild),)).fetchone()
            if row:
                question_id, question_text = row
                self.cursor.execute(update_entry_sql, (question_id,))
                await ctx.send(f"# QOTD: {question_text}")
            else:
                await ctx.send("No questions left! Add new questions or stop qotd...")
                return

async def setup(client):
    await client.add_cog(QuestionOfTheDay(client))