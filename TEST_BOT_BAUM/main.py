import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from discord.commands import Option
from discord.commands import slash_command

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

load_dotenv()
token = os.getenv("TOKEN")
if token is None:
    raise ValueError("TOKEN not found in .env file")

debug_guilds_up = []
server_token = os.getenv("SERVER").split(",")
for i in range(len(server_token)):
    debug_guilds_up.append(int(server_token[i]))
    
bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("!"),
    description="BaumSplitter41 Test Bot",
    intents=intents,
    debug_guilds=debug_guilds_up if debug_guilds_up else None
)

async def load_extensions():
    for filename in os.listdir("cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")   



class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

@bot.event
async def on_ready():
    print(f"{bot.user} ist online")

@bot.listen()
async def on_guild_join(guild):
    print(f"LOG: guild {guild} joined")


#---------------------------------------------------------------------------------------#
#DONT Touch anything above this line, unless you know what you are doing!#
#---------------------------------------------------------------------------------------#

#---------------------------------#
## Deleted Message
"""
@bot.event
async def on_message_delete(
    ctx = discord.Message,
):
    if ctx.author != bot.user:
        await ctx.send(f"Eine Nachricht von {ctx.author} wurde gelöscht: {ctx.content}", ephemeral=False)
"""
#---------------------------------#

#---------------------------------#
@bot.event
async def on_message_delete(msg):
    if msg.author != bot.user:  
        await msg.channel.send(f"A Message from {msg.author} has been deleted: {msg.content}")
#---------------------------------#

#---------------------------------#
## Greet
@bot.slash_command(description="Greet a User")
async def greet(ctx, user: str = Option(discord.User, "The user, you want to greet")):
    await ctx.respond(f"Hello {user.mention}")
#---------------------------------#

#---------------------------------#
## Say
@bot.slash_command(description="Let the bot send a message")
async def say(
        ctx,
        text: str = Option(description="Input the text you want to send"),
        channel_input: discord.TextChannel = Option(description="Select the channel,where you want to send the message.")
):  
    channel= discord.utils.get(ctx.guild.channels, id = int(channel_input[2:-1]))
    await channel.send(text)
    await ctx.respond("Message sent", ephemeral=True)
#---------------------------------#

#---------------------------------#
## Userinfo
@bot.slash_command(name="userinfo", description="Show informations of a user from this server")
async def info(
        ctx,
        user: str = Option(discord.User, "Select User"),
    ):
    if user is None:
        user = ctx.author
    elif user not in ctx.guild.members:
        await ctx.respond("The selected user is not a member on this Server!", ephemeral=True)
        return
    elif user == bot.user:
        await ctx.respond(f"This is me - the {bot.user}", ephemeral=True)
        return


    

    embed = discord.Embed(
        title=f"Information about *{user.name}*",
        description=f"Here you see all details about {user.mention}",
        color=discord.Color.blue()
    )

    time = discord.utils.format_dt(user.created_at, "R")

    embed.add_field(name="Account creation date", value=time, inline=False)
    if len(user.roles) >= 2:
        embed.add_field(name="Roles", value=", ".join([role.mention for role in user.roles if role.name != "@everyone"]), inline=False)
    else:
        embed.add_field(name="Roles", value="User has no roles", inline=False)
    embed.add_field(name="Server join date", value=discord.utils.format_dt(user.joined_at, "R"), inline=False)
    embed.add_field(name="User ID", value=user.id)

    embed.set_thumbnail(url=user.display_avatar.url)
    embed.set_author(name="World Wide Modding", icon_url="https://i.lcpdfrusercontent.com/uploads/monthly_2022_04/756701490_woldwidemodding.thumb.jpg.00bc1f61c05cc6d24519e1dda202d741.jpg")
    embed.set_footer(text="World Wide Modding - Bot | Made by BaumSplitter41")

    await ctx.respond(embed=embed)
#---------------------------------#

#---------------------------------#
## Serverinfo
@bot.slash_command(name="serverinfo", description = "Show Informations to this Server")
async def info(
    ctx,
):
    server = ctx.guild
    embed = discord.Embed(
        title=f"Serverinformations of __{server.name}__",
        description=f"Here you see all details about {server.name}",
        color=discord.Color.blue()
    )

    time = discord.utils.format_dt(server.created_at, "R")

    embed.add_field(name="Server creation date", value=time, inline=False)
    embed.add_field(name="Owner", value=server.owner, inline=False)
    embed.add_field(name="Member", value=server.member_count, inline=False)
    embed.add_field(name="Description", value=server.description, inline=False)
    
    embed.add_field(name="Server ID", value=server.id)

    embed.set_thumbnail(url=server.icon)
    embed.set_author(name="World Wide Modding", icon_url="https://i.lcpdfrusercontent.com/uploads/monthly_2022_04/756701490_woldwidemodding.thumb.jpg.00bc1f61c05cc6d24519e1dda202d741.jpg")
    embed.set_footer(text="World Wide Modding - Bot | Made by BaumSplitter41")

    await ctx.respond(embed=embed)
#---------------------------------#





bot.run(token)