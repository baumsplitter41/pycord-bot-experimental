import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from discord.commands import Option
from discord.commands import slash_command

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("!"),
    description="BaumSplitter41 Test Bot",
    intents=intents,
    #debug_guilds=[1423227652386455665],
    debug_guilds=[962718321655025684, 1423227652386455665]    # hier server id einfügen
)

async def load_extensions():
    for filename in os.listdir("cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")   

load_dotenv()
token = os.getenv("TOKEN")
if token is None:
    raise ValueError("TOKEN not found in .env file")


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


@bot.event
async def on_message_delete(msg):
    if msg.author != bot.user:
        await msg.channel.send(f"Eine Nachricht von {msg.author} wurde gelöscht: {msg.content}")




@bot.slash_command(description="Grüße einen User")
async def greet(ctx, user: str = Option(discord.User, "Der User, den du grüßen möchtest")):
    await ctx.respond(f"Hallo {user.mention}")


@bot.slash_command(description="Lass den Bot eine Nachricht senden")
async def say(
        ctx,
        text: str = Option(description="Der Text, den du senden möchtest"),
        channel: discord.TextChannel = Option(description="Der Channel, in den du die Nachricht senden möchtest")
):
    await channel.send(text)
    await ctx.respond("Nachricht gesendet", ephemeral=True)


@bot.slash_command(name="userinfo", description="Zeige Infos über einen User")
async def info(
        ctx,
        user: discord.Member = Option(description="Gib einen User an", default=None),
    ):
    if user is None:
        user = ctx.author

    embed = discord.Embed(
        title=f"Infos über {user.name}",
        description=f"Hier siehst du alle Details über {user.mention}",
        color=discord.Color.blue()
    )

    time = discord.utils.format_dt(user.created_at, "R")

    embed.add_field(name="Account erstellt", value=time, inline=False)
    embed.add_field(name="ID", value=user.id)

    embed.set_thumbnail(url=ctx.author.display_avatar.url)
    embed.set_footer(text="World Wide Modding - Bot")

    await ctx.respond(embed=embed)


@slash_command()
@commands.has_permissions(administrator=True)
async def hallo(self, ctx):
    await ctx.respond("Hey")

@commands.Cog.listener()
async def on_application_command_error(self, ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.respond(f"Nur Admins dürfen diesen Befehl ausführen!", ephemeral=True)
        return

    await ctx.respond(f"Es ist ein Fehler aufgetreten: ```{error}```", ephemeral=True)
    raise error






bot.run(token)