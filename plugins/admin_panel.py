import os, sys, time, asyncio, logging, datetime
from config import Config
from pyrogram import Client, filters
from helper.database import jishubotz
from pyrogram.types import Message
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid
from utils import send_log  # ✅ Make sure utils.py exists

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@Client.on_message(filters.command(["stats", "status", "s"]) & filters.user(Config.ADMIN))
async def get_stats(bot, message):
    total_users = await jishubotz.total_users_count()
    uptime = time.strftime("%Hh%Mm%Ss", time.gmtime(time.time() - bot.uptime))
    start_t = time.time()
    st = await message.reply('**Processing The Details.....**', quote=True)
    end_t = time.time()
    time_taken_s = (end_t - start_t) * 1000
    await st.edit(
        text=(
            "**--Bot Status--** \n\n"
            f"**⌚ Bot Uptime:** `{uptime}` \n"
            f"**🐌 Current Ping:** `{time_taken_s:.3f} ms` \n"
            f"**👭 Total Users:** `{total_users}`"
        )
    )


@Client.on_message(filters.command(["restart", "r"]) & filters.user(Config.ADMIN))
async def restart_bot(bot, message):
    msg = await bot.send_message(text="🔄 Processes Stopped. Bot Is Restarting...", chat_id=message.chat.id)
    await asyncio.sleep(3)
    await msg.edit("✅ Bot Is Restarted. Now You Can Use Me")
    os.execl(sys.executable, sys.executable, *sys.argv)


@Client.on_message(filters.private & filters.command(["ping", "p"]))
async def ping(_, message):
    start_t = time.time()
    rm = await message.reply_text("Pinging....", quote=True)
    end_t = time.time()
    time_taken_s = (end_t - start_t) * 1000
    await rm.edit(f"Ping 🔥!\n{time_taken_s:.3f} ms")
    return time_taken_s


@Client.on_message(filters.command(["broadcast", "b"]) & filters.user(Config.ADMIN) & filters.reply)
async def broadcast_handler(bot: Client, m: Message):
    await send_log(f"{m.from_user.mention} or {m.from_user.id} started a broadcast.")
    all_users = await jishubotz.get_all_users()
    broadcast_msg = m.reply_to_message
    sts_msg = await m.reply_text("Broadcast Started..!", quote=True)
    done = failed = success = 0
    start_time = time.time()
    total_users = await jishubotz.total_users_count()

    async for user in all_users:
        sts = await send_msg(user['_id'], broadcast_msg)
        if sts == 200:
            success += 1
        else:
            failed += 1
        if sts == 400:
            await jishubotz.delete_user(user['_id'])
        done += 1
        if done % 20 == 0:
            await sts_msg.edit(
                f"**Broadcast In Progress:** \n\n"
                f"Total Users: {total_users}\n"
                f"Completed: {done} / {total_users}\n"
                f"Success: {success}\n"
                f"Failed: {failed}"
            )

    completed_in = datetime.timedelta(seconds=int(time.time() - start_time))
    await sts_msg.edit(
        f"**Broadcast Completed:** \n\n"
        f"Completed In `{completed_in}`.\n\n"
        f"Total Users: {total_users}\n"
        f"Completed: {done} / {total_users}\n"
        f"Success: {success}\n"
        f"Failed: {failed}"
    )


async def send_msg(user_id, message):
    try:
        await message.copy(chat_id=int(user_id))
        return 200
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await send_msg(user_id, message)
    except (InputUserDeactivated, UserIsBlocked, PeerIdInvalid):
        logger.info(f"{user_id} : Unreachable (deactivated, blocked, or invalid)")
        return 400
    except Exception as e:
        logger.error(f"{user_id} : {e}")
        return 500
