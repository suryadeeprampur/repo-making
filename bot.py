from datetime import datetime
from pytz import timezone
from pyrogram import Client, __version__ as version
from pyrogram.raw.all import layer
from config import Config
from aiohttp import web
from route import web_server
import pyromod
import pyrogram.utils

pyrogram.utils.MIN_CHANNEL_ID = -100999999999999


class Bot(Client):

    def __init__(self):  # <-- Correct method name is __init__
        super().__init__(
            name="renamer",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            workers=200,
            plugins={"root": "plugins"},
            sleep_threshold=15,
        )

    async def start(self):
        await super().start()
        me = await self.get_me()
        self.mention = me.mention
        self.username = me.username
        self.uptime = Config.BOT_UPTIME

        if Config.WEBHOOK:
            app = web.AppRunner(await web_server())
            await app.setup()
            await web.TCPSite(app, "0.0.0.0", 8080).start()

        print(f"{me.first_name} Is Started.....✨️")

        for admin_id in Config.ADMIN:
            try:
                await self.send_message(admin_id, f"{me.first_name} Is Started...")
            except:
                pass

        if Config.LOG_CHANNEL:
            try:
                curr = datetime.now(timezone("Asia/Kolkata"))
                date = curr.strftime('%d %B, %Y')
                time = curr.strftime('%I:%M:%S %p')
                await self.send_message(
                    Config.LOG_CHANNEL,
                    f"{me.mention} Is Restarted !!\n\n📅 Date : {date}\n⏰ Time : {time}\n🌐 Timezone : Asia/Kolkata\n\n🉐 Version : v{version} (Layer {layer})"
                )
            except Exception as e:
                print("❌ Failed to send startup message to LOG_CHANNEL. Make sure the bot is admin there.")
                print(f"Error: {e}")

Bot().run()
# RDX Developer 
# Don't Remove Credit 🥺
# Telegram Channel @RDX_PVT_LTD
# Backup Channel @RDX_PVT_LTD
# Developer @RDX_PVT_LTD
# Contact @RDX1444
