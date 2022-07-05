from mimetypes import init
from socket import MsgFlag
from ssl import SSLContext
import requests
import json
import ssl
import websocket
import time
import asyncio

config = json.loads(open("channel.json").read())

dwebhook=config["discord"]["webhook"]
dtoken=config["discord"]["bot-token"]
dchannel=config["discord"]["channel-id"]
hapi=config["hummus"]["hummus-api"]
htoken=config["hummus"]["bot-token"]
hchannel=config["hummus"]["channel-id"]

def init_authentication(token):
    ws = websocket.WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})
    ws.connect("wss://hummus-stg-gateway.sys42.net")
    print(ws.recv())
    print("Authenticating....")
    body = str({
        "token": token,
        "properties": {
            "$os": "whatsitoya",
            "$browser": "hummus.py",
            "$device": "hummus.py",
            "$referrer": "",
            "$referring_domain": ""
        },
        "compress": "false",
        "large_threshold": "250",
        "shart": "[1, 10]"
    })
    ws.send(body)
    print(ws.recv())
    ws.close()

def get_messages(cid, limit):
    result = requests.get(hapi+"channels/"+str(cid)+"/messages",
        headers = {"Authorization": "Bot OTkzNzM1OTc3MDkzNTkxMDQy.YrAAvg.q0H1fua5NlaK9dJqnVgDb-Eeh1vC-h07zE9ZdQ"},
        json = {"limit": limit}
    )
    return result.json()
def send_message(cid, text):
    result = requests.post(hapi+"channels/"+str(cid)+"/messages",
        headers = {"Authorization": "Bot OTkzNjMwOTM0NDAzNDExOTY5.Yq_Law.z0JOUgjoLQt3M4UUm3Noj2vDJhLewFZoVS605A"},
        json = {
            "content": text
        } 
    )
    return result.json()
def get_channel(id):
    result = requests.get(hapi+"channels/"+str(id), headers= {
        "Authorization": "Bot "
    })
    return result.json()

def main():
    screamo = 0
    lastmessage = None;
    init_authentication(htoken)
    while True:
        screamo+=1
        try:
            if screamo == 10:
                requests.post(
                    dwebhook,
                    json = {
                        "username": "Clyde",
                        "content": "Please don't crash the bot",
                        "avatar_url": "https://discord.com/assets/18126c8a9aafeefa76bbb770759203a9.png"
                    }
                )
                screamo = 0
            if lastmessage != get_messages(hchannel, 1)[0]:
                if (lastmessage != None):
                    old_id = lastmessage["id"]
                else:
                    old_id = 0

                print("!!!")
                lastmessage = get_messages(hchannel, 1)[0]

                embeds = None
                msgattach = ""
                if (lastmessage["attachments"] != []):
                    for image in lastmessage["attachments"]:
                        if str(image["filename"]).lower().endswith("png") or str(image["filename"]).lower().endswith("jpg") or str(image["filename"]).lower().endswith("jpeg") or str(image["filename"]).lower().endswith("gif") or str(image["filename"]).lower().endswith("gifv") or str(image["filename"]).lower().endswith("webm") or str(image["filename"]).lower().endswith("mp4"):
                            msgattach+=" [ ]("+image["url"]+")"
                        else:
                            embeds = [{
                                "title": image["filename"],
                                "description": str(round(image["size"] / 1024)) + " kilobyte file\n[` Download attachment `]("+image["url"]+")",
                                "color": "16711935",
                                "url": image["url"]
                            }]

                if (old_id != lastmessage["id"]):
                    if (lastmessage["author"]["bot"] != True):
                        response = requests.post(
                            dwebhook,
                            json = {
                                "username": lastmessage["author"]["username"],
                                "content": lastmessage["content"]+msgattach,
                                "avatar_url": "https://hummus-stg-cdn.sys42.net/avatars/"+lastmessage["author"]["id"]+"/user_avatar.png",
                                "embeds": embeds
                            }
                        )
                        print(response)
                else:
                    print("Ignoring edit")
        except (IndexError):
            # doddle
            print("",sep="",end="")

main()