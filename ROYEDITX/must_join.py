from config import MUST_JOIN
import logging

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors import ChatAdminRequired, UserNotParticipant, ChatWriteForbidden


@Client.on_message(filters.incoming & filters.private, group=-1)
async def must_join_channel(bot: Client, msg: Message):
    if not MUST_JOIN:
        return
    try:
        raw = str(MUST_JOIN).strip()
        try:
            if raw.startswith("-") or raw.isdigit():
                chat_id = int(raw)
            else:
                chat_id = raw
        except ValueError:
            chat_id = raw

        try:
            await bot.get_chat_member(chat_id, msg.from_user.id)
        except UserNotParticipant:
            link = None
            if isinstance(chat_id, str) and not chat_id.startswith("-") and not chat_id.isdigit():
                username = chat_id.lstrip("@")
                link = f"https://t.me/{username}"
            else:
                try:
                    chat_info = await bot.get_chat(chat_id)
                    link = chat_info.invite_link
                except Exception:
                    link = None

            if not link:
                if isinstance(chat_id, int) or (isinstance(chat_id, str) and chat_id.startswith("-")):
                    clean_id = str(chat_id).replace("-100", "").replace("-", "")
                    link = f"https://t.me/c/{clean_id}"
                else:
                    link = f"https://t.me/{str(chat_id).lstrip('@')}"

            try:
                await msg.reply_photo(
                    photo="https://telegra.ph/file/4bd4e28e31194e1820bf5.jpg",
                    caption=f"❖ ғɪʀsᴛʟʏ ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ᴊᴏɪɴ ᴏᴜʀ ғᴀᴍɪʟʏ ➥ [sᴜᴘᴘᴏʀᴛ]({link}) ᴛʜᴇɴ ʏᴏᴜ ᴄᴀɴ ᴜsᴇ ᴍᴇ,",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ", url=link),
                            ]
                        ]
                    )
                )
                await msg.stop_propagation()
            except ChatWriteForbidden:
                pass
    except ChatAdminRequired:
        print(f"❖ ᴘʀᴏᴍᴏᴛᴇ ᴍᴇ ᴀs ᴀ ᴀᴅᴍɪɴ ɪɴ ᴍᴜsᴛ_ᴊᴏɪɴ ᴄʜᴀᴛ ➥ {MUST_JOIN} !")
    except Exception as e:
        logging.warning(f"Error in must_join_channel: {e}")
