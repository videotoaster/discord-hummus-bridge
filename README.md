# discord-hummus-bridge
A bridge between [Hummus](https://hummus.sys42.net/) and [Discord](https://discord.com).

## Setup
1) [Click here](https://hummus.sys42.net/developers/applications) and create a new application
2) Name it and provide the avatar it will use on the Hummus side
3) Create a bot account for the application (DO NOT TOUCH ANYTHING other than Copy Token)
4) Open channel.json, find the "bot-token" key under Hummus, set it to your copied token
5) [Click here](https://discord.com/developers/applications) and do the same again
6) Copy the Discord bot token to the Discord bot-token key
7) Go into the channel you want to bridge's settings on Discord
8) Go into Integrations and create a webhook
9) Give the webhook an avatar - it will use this when a Hummus user doesn't have one
10) Copy the webhook URL to the channel.json file - under "webhook"
11) Right-click the channel you want to bridge, hit "Copy ID", and paste it under the first channel-id key
12) Right-click the channel you want to bridge on Hummus, hit "Copy ID", and paste it under the second channel-id key
13) Go back to the Hummus developer page where you made the bot
14) Click "OAuth 2 URL Generator" and DO NOT TOUCH ANYTHING other than the button to generate the URL
15) Visit the URL and invite the bot to your Hummus server
16) Go to the Discord developer page where you made the bot
17) Copy the Client ID
18) Type https://discord.com/api/oauth2/authorize?client_id=[the client ID you copied]&permissions=8&scope=bot&applications.commands
19) Add the bot to your Discord server
20) Start both of the scripts on your desktop - it should work??? I don't know man. I'm too tired for this shit
