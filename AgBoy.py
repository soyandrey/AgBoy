# This example requires the 'members' privileged intents

import discord
from discord.ext import commands
import random
import asyncio
import datetime

description = '''un bot para algo que no se que'''

intents = discord.Intents.default()
intents.members = True
time_window_milliseconds = 5000
max_msg_per_window = 5
author_msg_times = {}

bot = commands.Bot(command_prefix='?', description=description, intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)

@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)

@bot.command(description='For when you wanna settle the score some other way')
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))

@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await ctx.send(content)

@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send(f'{member.name} joined in {member.joined_at}')

@bot.group()
async def cool(ctx):
    """Says if a user is cool.
    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:
        await ctx.send(f'No, {ctx.subcommand_passed} is not cool')

@cool.command(name='bot')
async def _bot(ctx):
    """Is the bot cool?"""
    await ctx.send('Yes, the bot is cool.')


@bot.event
async def on_message(msg):
    global author_msg_counts

    author_id = msg.author.id
    # Get current epoch time in milliseconds
    curr_time = datetime.datetime.now().timestamp() * 1000

    # Make empty list for author id, if it does not exist
    if not author_msg_times.get(author_id, False):
        author_msg_times[author_id] = []

    # Append the time of this message to the users list of message times
    author_msg_times[author_id].append(curr_time)

    # Find the beginning of our time window.
    expr_time = curr_time - time_window_milliseconds

    # Find message times which occurred before the start of our window
    expired_msgs = [
        msg_time for msg_time in author_msg_times[author_id]
        if msg_time < expr_time
    ]

    # Remove all the expired messages times from our list
    for msg_time in expired_msgs:
        author_msg_times[author_id].remove(msg_time)
    # ^ note: we probably need to use a mutex here. Multiple threads
    # might be trying to update this at the same time. Not sure though.

    if len(author_msg_times[author_id]) > max_msg_per_window:
       await msg.author.send("""Kicked from **""" + msg.guild.name + """** avoid from spamming
       Please stop spamming and respect our rules
       
       >**an error?**: just join but be careful.
       >**Hacked account?**: we dont make responsable of your account""")
       await msg.guild.ban(msg.author, reason="spamming 5msg / 5sec")
       await asyncio.sleep(5)
       await msg.guild.unban(msg.author, reason="spamming 5msg / 5sec")
       print("Spammer kicked")


@bot.event
async def on_member_join(member):
        created = member.created_at
        now = datetime.now() # remember to `from datetime import datetime`
        delta = (now - created).days
        print("time:" + delta)
        channel = "general"     
        print("channel")
        if delta < 10:
         await member.kick()
         await channel.send('Detected alt account and kicked it')
         await channel.send(f"> :no_entry: {member.mention} Alt account detected")
         await member.send("""
         :no_entry: Your account has been blocked on 

         > **Blocked by:** Bot (AgBoy AntiAlt)

         > **Reason:** we believe that this is an alt account.
 
         > **What does that mean?** You don't have full access to
         > certain features of both the Discord server and the
         > Minecraft server, e.g. writing in Channels, at least on
         > this account.

         > **False-positive! I'm innocent!** If this is NOT an alt account,
         > we apologize for this. Contact us and don't worry.

         > **When do I get unblocked?** If this is in fact an alt account,
         >  don't be suprised if we even KICK or BAN you.

            """)
        else:
         pass


bot.run('the token here')
