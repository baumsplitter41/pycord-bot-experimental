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
        await msg.channel.send(f"Eine Nachricht von {msg.author} wurde gelöscht: {msg.content}")
#---------------------------------#

#---------------------------------#
## Greet
@bot.slash_command(description="Grüße einen User")
async def greet(ctx, user: str = Option(discord.User, "Der User, den du grüßen möchtest")):
    await ctx.respond(f"Hallo {user.mention}")
#---------------------------------#

#---------------------------------#
## Say
@bot.slash_command(description="Lass den Bot eine Nachricht senden")
async def say(
        ctx,
        text: str = Option(description="Der Text, den du senden möchtest"),
        channel_input: discord.TextChannel = Option(description="Der Channel, in den du die Nachricht senden möchtest")
):  
    channel= discord.utils.get(ctx.guild.channels, id = int(channel_input[2:-1]))
    await channel.send(text)
    await ctx.respond("Nachricht gesendet", ephemeral=True)
#---------------------------------#

#---------------------------------#
## Userinfo
@bot.slash_command(name="userinfo", description="Zeige Infos über einen User")
async def info(
        ctx,
        user: str = Option(discord.User, "Select User"),
    ):
    if user is None:
        user = ctx.author
    elif user not in ctx.guild.members:
        await ctx.respond("Der User ist nicht auf diesem Server!", ephemeral=True)
        return
    elif user == bot.user:
        await ctx.respond("Das bin ja ich!", ephemeral=True)
        return


    

    embed = discord.Embed(
        title=f"Infos über {user.name}",
        description=f"Hier siehst du alle Details über {user.mention}",
        color=discord.Color.blue()
    )

    time = discord.utils.format_dt(user.created_at, "R")

    embed.add_field(name="Account erstellt", value=time, inline=False)
    embed.add_field(name="Rollen", value=", ".join([role.mention for role in user.roles if role.name != "@everyone"]), inline=False)
    embed.add_field(name="Server Join", value=discord.utils.format_dt(user.joined_at, "R"), inline=False)
    embed.add_field(name="ID", value=user.id)

    embed.set_thumbnail(url=user.display_avatar.url)
    embed.set_footer(text="World Wide Modding - Bot | Made by BaumSplitter41")

    await ctx.respond(embed=embed)
#---------------------------------#

#---------------------------------#
## Serverinfo
"""@bot.slash_command(name="Serverinfo", description = "Show Informations to this Server")
async def info(
    ctx,
    server = discord.guild
):

    embed = discord.Embed(
        title=f"Infos über {server.name}",
        description=f"Hier siehst du alle Details über {server.mention}",
        color=discord.Color.blue()
    )


    await ctx.respond(embed=embed)


"""
#---------------------------------#





bot.run(token)