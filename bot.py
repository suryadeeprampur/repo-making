from datetime import datetime
from pytz import timezone
from pyrogram import Client, __version__ as version  # ✅ fixed import
from pyrogram.raw.all import layer
from config import Config
from aiohttp import web
from route import web_server
import pyromod
import pyrogram.utils

# Minimum channel ID adjustment (Pyrogram tweak)
pyrogram.utils.MIN_CHANNEL_ID = -100999999999999


class Bot(Client):
    def __init__(self):
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

        print(f"{me.first_name} is Started.....✨️")
        print(f"Running Pyrogram v{version} | Layer {layer}")

        # Send startup message to each admin
        for admin_id in Config.ADMIN:
            try:
                await self.send_message(admin_id, f"✅ {me.first_name} is Started...")
            except Exception as e:
                print(f"❌ Couldn't send start message to admin {admin_id}: {e}")

        # Webhook (if enabled)
        if Config.WEBHOOK:
            try:
                app = web.AppRunner(await web_server())
                await app.setup()
                await web.TCPSite(app, "0.0.0.0", 8080).start()
                print("✅ Webhook server started on port 8080")
            except Exception as e:
                print(f"❌ Failed to start webhook server: {e}")

        # Log channel startup message
        if Config.LOG_CHANNEL:
            try:
                curr = datetime.now(timezone("Asia/Kolkata"))
                date = curr.strftime('%d %B, %Y')
                time_str = curr.strftime('%I:%M:%S %p')
                await self.send_message(
                    Config.LOG_CHANNEL,
                    f"{me.mention} is Restarted !!\n\n📅 Date : {date}\n⏰ Time : {time_str}\n🌐 Timezone : Asia/Kolkata\n\n🉐 Version : v{version} (Layer {layer})"
                )
            except Exception as e:
                print("❌ Failed to send message to LOG_CHANNEL.")
                print(f"Error: {e}")


# Start the bot
Bot().run()
# RDX Developer 
# Don't Remove Credit 🥺
# Telegram Channel @RDX_PVT_LTD
# Backup Channel @RDX_PVT_LTD
# Developer @RDX_PVT_LTD
# Contact @RDX1444
