# Imports
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

# Load token and id from .env
load_dotenv()
token = os.getenv('token')
clientid = os.getenv('botid')

# Intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.messages = True

# Bot Setup
bot = commands.Bot(command_prefix="b! ", intents=intents)

# Functions

class SOTWButtons(discord.ui.View):
    def __init__(self, panda_id, cats_id, bamboot_id):
        super().__init__(timeout=None)
        
        self.p_id = panda_id
        self.c_id = cats_id
        self.b_id = bamboot_id

    @discord.ui.button(label="Panda", style=discord.ButtonStyle.blurple)
    async def panda_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        user = interaction.guild.get_member(self.p_id)
        name = user.display_name if user else "Panda"
        await interaction.response.send_message("You voted {name} for Staff of The Week.", ephemeral=True)

    @discord.ui.button(label="Cats", style=discord.ButtonStyle.blurple)
    async def cats_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        user = interaction.guild.get_member(self.c_id)
        name = user.display_name if user else "Cats"
        await interaction.response.send_message("You voted {name} for Staff of The Week.", ephemeral=True)

    @discord.ui.button(label="Bamboot", style=discord.ButtonStyle.blurple)
    async def bamboot_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        user = interaction.guild.get_member(self.b_id)
        name = user.display_name if user else "Bamboot"
        await interaction.response.send_message("You voted {name} for Staff of The Week.", ephemeral=True)

# Commands

@bot.command(name="sotw")
@commands.has_role(1443544544409948272)
async def sotw(ctx):
    channel_id = 1479877488510500956
    channel = bot.get_channel(channel_id)
    panda = 502141502038999041
    cats = 972943470023041044
    bamboot = 1479571065549357362
    ctx=ctx

    embed = discord.Embed(
        title="Staff of The Week",
        description="Staff of The Week!\n \nVote for this weeks best staff!\n \nThis weeks choices are:\nWebThePanda (Owner)\nCats (Cool Guy)\nBamboot (Bot)",
        colour=discord.Color.blurple()
    )

    if channel:
        view = SOTWButtons(panda_id=panda, cats_id=cats, bamboot_id=bamboot)
        await channel.send(embed=embed, view=view)
        await ctx.send("Poll made successfully!")

@bot.command(name="purge")
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount: int):
    if amount <= 0:
        await ctx.send("Please specify a number greater than zero.")
        return
    
    try:
        deleted = await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"Purged {len(deleted) - 1} messages.", delete_after=5)
    except discord.Forbidden:
        await ctx.send("I do not have the 'Manage Messages' permission to do this.")
    except Exception as e:
        await ctx.send(f"An error occured: {e}")


# Events

@bot.event
async def on_member_join(member):
    channel_id = 1443544545261518850
    channel = bot.get_channel(channel_id)
    embed = discord.Embed(
        title="Welcome to the community. 🐼",
        description=f"Welcome {member} to the community server of WebThePanda. I hope you enjoy your stay.",
        color=discord.Color.pink()
    )
    embed.set_author(
        name=f"New Member: {member.display_name}",
        icon_url=member.display_avatar.url
    )
    
    if channel:
        await channel.send(embed=embed)

# Error

@purge.error
async def purge_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have the 'Manage Messages' permission to use this command.")

bot.run(token)