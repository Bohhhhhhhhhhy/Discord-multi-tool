import os
import aiohttp
import asyncio
from pystyle import Colors,Colorate
from colorama import Fore

os.system("title Honoured DMspam")

banner = """
                               
                                   ░██████╗░░█████╗░░░░░░██╗░█████╗░
                                   ██╔════╝░██╔══██╗░░░░░██║██╔══██╗
                                   ██║░░██╗░██║░░██║░░░░░██║██║░░██║
                                   ██║░░╚██╗██║░░██║██╗░░██║██║░░██║
                                   ╚██████╔╝╚█████╔╝╚█████╔╝╚█████╔╝
                                   ░╚═════╝░░╚════╝░░╚════╝░░╚════╝░
                                              DM spam

"""

print(Colorate.Vertical(Colors.blue_to_purple,banner,1,0))
user_id = int(input((Colorate.Vertical(Colors.blue_to_purple," [+] User ID: ",1,0))))
msg = input(Colorate.Vertical(Colors.blue_to_purple," [+] Message to send: ",1,0))
tokens = open("bot_tokens.txt","r").read().splitlines()

async def dm_spam(token):
    headers = {
        "Authorization": f"Bot {token}"
    }
    payload = {
        "recipients": [user_id]
    }

    async with aiohttp.ClientSession() as session:
        async with session.post("https://discord.com/api/v9/users/@me/channels", headers=headers, json=payload) as r:
            if r.status == 200:
                a = await r.json()
                id = a["id"]
                if not id:
                    print(Fore.RED + " [+] Failed to create DM channel!\n" + Fore.RESET)
                    return
            else:
                print(Fore.RED + f" [+] Failed to create DM channel: {r.status}\n" + Fore.RESET)
                return
        
        payload2 = {
            "content": msg
        }

        while True:
            async with session.post(f"https://discord.com/api/v9/channels/{id}/messages", headers=headers, json=payload2) as req:
                if req.status in [200, 201, 204]:
                    print(Fore.GREEN + " [+] Message Sent!\n" + Fore.RESET)
                elif req.status == 429:
                    print(Fore.RED + " [+] Rate Limited!\n" + Fore.RESET)
                    retry_after = (await req.json()).get('retry_after', 1)
                    await asyncio.sleep(retry_after)
                else:
                    print(Fore.RED + f" [+] Error {req.status}!\n" + Fore.RESET)
                    break

async def execute():
    tasks = [dm_spam(token) for token in tokens]
    await asyncio.gather(*tasks)

asyncio.run(execute())
