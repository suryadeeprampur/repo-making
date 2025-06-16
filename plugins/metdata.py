from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from helper.database import jishubotz
from pyromod.exceptions import ListenerTimeout
from config import Txt



ON = [[InlineKeyboardButton('Metadata On ✅', callback_data='metadata_1')], [
    InlineKeyboardButton('Set Custom Metadata', callback_data='cutom_metadata')]]
OFF = [[InlineKeyboardButton('Metadata Off ❌', callback_data='metadata_0')], [
    InlineKeyboardButton('Set Custom Metadata', callback_data='cutom_metadata')]]


@Client.on_message(filters.private & filters.command('metadata'))
async def handle_metadata(bot: Client, message: Message):

    ms = await message.reply_text("**Please Wait...**", reply_to_message_id=message.id)
    bool_metadata = await jishubotz.get_metadata(message.from_user.id)
    user_metadata = await jishubotz.get_metadata_code(message.from_user.id)
    await ms.delete()
    if bool_metadata:
        return await message.reply_text(f"**Your Current Metadata :-**\n\n➜ `{user_metadata}` ",quote=True, reply_markup=InlineKeyboardMarkup(ON))
    return await message.reply_text(f"**Your Current Metadata :-**\n\n➜ `{user_metadata}` ",quote=True, reply_markup=InlineKeyboardMarkup(OFF))


@Client.on_callback_query(filters.regex('.*?(custom_metadata|metadata).*?'))
async def query_metadata(bot: Client, query: CallbackQuery):

    data = query.data

    if data.startswith('metadata_'):
        _bool = data.split('_')[1]
        user_metadata = await jishubotz.get_metadata_code(query.from_user.id)

        if bool(eval(_bool)):
            await jishubotz.set_metadata(query.from_user.id, bool_meta=False)
            await query.message.edit(f"**Your Current Metadata :-**\n\n➜ `{user_metadata}` ", reply_markup=InlineKeyboardMarkup(OFF))

        else:
            await jishubotz.set_metadata(query.from_user.id, bool_meta=True)
            await query.message.edit(f"**Your Current Metadata :-**\n\n➜ `{user_metadata}` ", reply_markup=InlineKeyboardMarkup(ON))

    elif data == 'cutom_metadata':
        await query.message.delete()
        try:
            try:
                metadata = await bot.ask(text=Txt.SEND_METADATA, chat_id=query.from_user.id, filters=filters.text, timeout=30, disable_web_page_preview=True, reply_to_message_id=query.message.id)
            except ListenerTimeout:
                await query.message.reply_text("⚠️ Error !!\n\n**Request Timed Out.**\n\nRestart By Using /metadata", reply_to_message_id=query.message.id)
                return
            print(metadata.text)
            ms = await query.message.reply_text("**Please Wait...**", reply_to_message_id=metadata.id)
            await jishubotz.set_metadata_code(query.from_user.id, metadata_code=metadata.text)
            await ms.edit("**Your Metadata Code Set Successfully ✅**")
        except Exception as e:
            print(e)



# RDX Developer 
# Don't Remove Credit 🥺
# Telegram Channel @RDX_PVT_LTD
# Backup Channel @RDX_PVT_LTD
# Developer @RDX_PVT_LTD
# Contact @RDX1444
