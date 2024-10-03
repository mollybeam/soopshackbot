import discord
from discord.ext import commands
from discord import app_commands
import random

intents = discord.Intents.default()
intents.message_content = True

with open("token.txt") as tfd:
    TOKEN = tfd.readline().strip("\r\n ")
    
with open("disconnectable_users.txt") as tfd:
    DISCONNECTABLE_USERS = []
    DISCONNECTABLE_USERS.append(int(tfd.readline()))

# bot = commands.Bot(command_prefix='$', intents=intents)

MY_GUILD = discord.Object(783926648890064906)

class SoopShackBotClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        # A CommandTree is a special type that holds all the application command
        # state required to make it work. This is a separate class because it
        # allows all the extra state to be opt-in.
        # Whenever you want to work with application commands, your tree is used
        # to store and work with them.
        # Note: When using commands.Bot instead of discord.Client, the bot will
        # maintain its own tree instead.
        self.tree = app_commands.CommandTree(self)
        
    # In this basic example, we just synchronize the app commands to one guild.
    # Instead of specifying a guild to every command, we copy over our global commands instead.
    # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)
        
        
intents = discord.Intents.default()
client = SoopShackBotClient(intents=intents)


@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')


@client.tree.command()
async def add(interaction: discord.Interaction, left: int, right: int):
    """Adds two numbers together."""
    await interaction.response.send_message(left + right)


@client.tree.command()
async def roll(interaction: discord.Interaction, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await interaction.response.send_message('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await interaction.response.send_message(result)


@client.tree.command()
async def joined(interaction: discord.Interaction, member: discord.Member):
    """Says when a member joined."""
    await interaction.response.send_message(f'{member.name} joined {discord.utils.format_dt(member.joined_at)}')


@client.tree.command()
async def disconnect(interaction: discord.Interaction, member: discord.Member):
    """disconnects a member from their current voice channel"""
    if member.id in [DISCONNECTABLE_USERS]:
        try:
            await member.move_to(channel = None, reason="Requested by command")
            await interaction.response.send_message(f"Disconnected {member}")
        except Exception as e:
            print(e, e.args)
    else:
        await interaction.response.send_message(f"User {member} not in disconnect list")

client.run(TOKEN)


