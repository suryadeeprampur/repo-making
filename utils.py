import math, time, re, os, shutil

from datetime import datetime

from pytz import timezone

from config import Config, Txt 

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup





async def progress_for_pyrogram(current, total, ud_type, message, start):

    now = time.time()

    diff = now - start

    if int(diff) % 5 == 0 or current == total:        

        percentage = current * 100 / total

        speed = current / diff

        elapsed_time = round(diff) * 1000

        time_to_completion = round((total - current) / speed) * 1000

        estimated_total_time = elapsed_time + time_to_completion



        elapsed_str = TimeFormatter(milliseconds=elapsed_time)

        estimated_str = TimeFormatter(milliseconds=estimated_total_time)



        progress = "{0}{1}".format(

            ''.join(["▣" for _ in range(math.floor(percentage / 5))]),

            ''.join(["▢" for _ in range(20 - math.floor(percentage / 5))])

        )



        tmp = progress + Txt.PROGRESS_BAR.format(

            round(percentage, 2),

            humanbytes(current),

            humanbytes(total),

            humanbytes(speed),

            estimated_str if estimated_str else "0 s"

        )

        try:

            await message.edit(

                text=f"{ud_type}\n\n{tmp}",

                reply_markup=InlineKeyboardMarkup([

                    [InlineKeyboardButton("✖️ Cancel ✖️", callback_data="close")]

                ])

            )

        except:

            pass





def humanbytes(size):    

    if not size:

        return "0 B"

    power = 2**10

    n = 0

    Dic_powerN = {0: '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}

    while size >= power and n < 4:

        size /= power

        n += 1

    return f"{round(size, 2)} {Dic_powerN[n]}B"





def TimeFormatter(milliseconds: int) -> str:

    seconds, milliseconds = divmod(int(milliseconds), 1000)

    minutes, seconds = divmod(seconds, 60)

    hours, minutes = divmod(minutes, 60)

    days, hours = divmod(hours, 24)

    tmp = (

        (f"{days}d, " if days else "") +

        (f"{hours}h, " if hours else "") +

        (f"{minutes}m, " if minutes else "") +

        (f"{seconds}s, " if seconds else "") +

        (f"{milliseconds}ms, " if milliseconds else "")

    )

    return tmp.rstrip(', ')





def convert(seconds):

    seconds %= (24 * 3600)

    hour = seconds // 3600

    seconds %= 3600

    minutes = seconds // 60

    seconds %= 60      

    return f"{hour}:{minutes:02d}:{seconds:02d}"





async def send_log(b, u):

    if Config.LOG_CHANNEL:

        curr = datetime.now(timezone("Asia/Kolkata"))

        date = curr.strftime('%d %B, %Y')

        time_str = curr.strftime('%I:%M:%S %p')

        await b.send_message(

            Config.LOG_CHANNEL,

            (

                f"<b><u>New User Started The Bot :</u></b>\n\n"

                f"<b>User Mention</b> : {u.mention}\n"

                f"<b>User ID</b> : `{u.id}`\n"

                f"<b>First Name</b> : {u.first_name}\n"

                f"<b>Last Name</b> : {u.last_name}\n"

                f"<b>User Name</b> : @{u.username}\n"

                f"<b>User Link</b> : <a href='tg://openmessage?user_id={u.id}'>Click Here</a>\n\n"

                f"<b>Date</b> : {date}\n"

                f"<b>Time</b> : {time_str}"

            )

        )





def add_prefix_suffix(input_string, prefix='', suffix=''):

    pattern = r'(?P<filename>.*?)(\.\w+)?$'

    match = re.search(pattern, input_string)

    if match:

        filename = match.group('filename')

        extension = match.group(2) or ''

        result = f"{prefix}{filename}"

        if suffix:

            result += f" {suffix}"

        return result + extension

    return input_string





def makedir(name: str):

    """

    Create a directory with the specified name.

    If a directory with the same name already exists, it will be removed and a new one will be created.

    """

    if os.path.exists(name):

        shutil.rmtree(name)

    os.mkdir(name)





# RDX Developer 

# Don't Remove Credit 🥺

# Telegram Channel @RDX_PVT_LTD

# Backup Channel @RDX_PVT_LTD

# Developer @RDX_PVT_LTD

# Contact @RDX1444
