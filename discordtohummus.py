import discord
import requests
import websocket
import json
import ssl

config = json.loads(open("channel.json").read())
dwebhook=config["discord"]["webhook"]
dtoken=config["discord"]["bot-token"]
dchannel=config["discord"]["channel-id"]
hapi=config["hummus"]["hummus-api"]
htoken=config["hummus"]["bot-token"]
hchannel=config["hummus"]["channel-id"]

# Hummus requires authentication with the
# gateway websocket at least once.
def init_authentication(token):
    ws = websocket.WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})
    ws.connect("wss://hummus-stg-gateway.sys42.net")
    print(ws.recv())
    body = str({
        "token": token,
        "properties": {
            "$os": "PenisOS",
            "$browser": "hummus.py",
            "$device": "hummus.py",
            "$referrer": "",
            "$referring_domain": ""
        },
        "compress": "false",
        "large_threshold": "250",
        "shard": "[1, 10]"
    })
    ws.send(body)
    print(ws.recv())
    ws.close()
# Send a Hummus message
def send_message(cid, text):
    result = requests.post(hapi+"channels/"+str(cid)+"/messages",
        headers = {"Authorization": "Bot "+htoken},
        json = {
            "content": text
        } 
    )
    return result.json()

# Discord bits
class DiscordToHummusBridge(discord.Client):
    async def on_ready(self):
        init_authentication(htoken)
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        
    async def on_message(self, message):
        if (message.webhook_id == None):
            send_message(hchannel, f"**{message.author.name}:**\n{message.content}")
        else:
            print(message.webhook_id)


intents = discord.Intents.default()
intents.members = True

client = DiscordToHummusBridge(intents=intents)
client.run(dtoken)