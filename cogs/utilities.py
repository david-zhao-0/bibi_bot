from discord import Forbidden
from discord.ext import tasks, commands
import random
from datetime import datetime, timezone
import pytz
import aiosqlite

EST = pytz.timezone("US/Eastern")

class Utilities(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.check_reminders.start()

    @commands.command()
    async def flip_coin(self, ctx):
        await ctx.send(random.choice(["Heads", "Tails"]))

    @commands.command()
    async def choose_from(self, ctx, *, selection:str):
        choices = selection.strip().split(" ")
        if len(choices) < 2:
            await ctx.send(f"Cannot randomly choose between {len(choices)} choices!")
        else:
            await ctx.send(random.choice(choices))

    @commands.command()
    @commands.has_guild_permissions(manage_channels=True)
    async def purge(self, ctx, n_messages):
        try:
            n_messages = int(n_messages)
        except ValueError:
            await ctx.send("Invalid number of messages to purge.")
        if n_messages > 0:
            deleted = await ctx.channel.purge(limit=n_messages)
            await ctx.send(f"Deleted {len(deleted)} messages.")
        else:
            await ctx.send(f"Cannot purge {n_messages} messages.")

    @commands.command()
    async def set_reminder(self, ctx, reminder_time: str, *, message : str):

        try:
            parsed_time = datetime.strptime(reminder_time, "%H:%M").time()
        except ValueError:
            await ctx.send("Invalid time format. Use HH:MM (24-hour)")
            return
        
        now = datetime.now(EST)
        dt_est = datetime.combine(now.date(), parsed_time)
        dt_utc = EST.localize(dt_est).astimezone(pytz.utc)
        utc_time_str = dt_utc.strftime("%H:%M")

        async with aiosqlite.connect("data/reminders.db") as db:
            await db.execute(
                """INSERT INTO reminders (user_id, reminder_time, message, timezone) 
                VALUES (?, ?, ?, ?)""", (str(ctx.author.id), utc_time_str, message, "US/Eastern")
            )
            await db.commit()
        
        await ctx.send(f"Reminder set for {reminder_time} EST daily: {message}. Look out for it in your DMs!")

    @commands.command()
    async def cancel_reminders(self, ctx):
        async with aiosqlite.connect("data/reminders.db") as db:
            await db.execute("""DELETE FROM reminders WHERE user_id = ?""", (str(ctx.author.id),))
            await db.commit()
        await ctx.send("All your reminders have been cancelled.")

    @tasks.loop(minutes=1)
    async def check_reminders(self):
        now_utc = datetime.now(pytz.utc).strftime("%H:%M")
        async with aiosqlite.connect("data/reminders.db") as db:
            async with db.execute(
                """SELECT user_id, message FROM reminders WHERE reminder_time = ?""",
                (now_utc,)
            ) as cursor:
                rows = await cursor.fetchall()

        for user_id, message in rows:
            user = self.client.get_user(int(user_id))
            if user:
                try:
                    await user.send(f"Reminder: {message}")
                except Forbidden:
                    print(f"Couldn't DM user {user_id}")
                
async def setup(client):
    await client.add_cog(Utilities(client))