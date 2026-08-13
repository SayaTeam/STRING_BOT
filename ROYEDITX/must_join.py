from config import MUST_JOIN, OWNER_ID
import logging

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import ChatAdminRequired, UserNotParticipant, ChatWriteForbidden, PeerIdInvalid, UsernameInvalid


@Client.on_message(filters.incoming & filters.private, group=-1)
async def must_join_channel(bot: Client, msg: Message):
    if not MUST_JOIN:
        return
    if msg.from_user and msg.from_user.id == OWNER_ID:
        return

    raw = str(MUST_JOIN).strip().lstrip("@")
    if not raw:
        return

    if raw.startswith("-") or raw.isdigit():
        try:
            chat_id = int(raw)
        except ValueError:
            chat_id = raw
    else:
        chat_id = raw

    user_id = msg.from_user.id if msg.from_user else None
    if not user_id:
        return

    is_joined = False
    try:
        member = await bot.get_chat_member(chat_id, user_id)
        if member.status not in [ChatMemberStatus.LEFT, ChatMemberStatus.BANNED]:
            is_joined = True
    except UserNotParticipant:
        is_joined = False
    except (ChatAdminRequired, PeerIdInvalid, UsernameInvalid) as e:
        logging.warning(f"MUST_JOIN admin/chat issue for '{MUST_JOIN}': {e}")
        return
    except Exception as e:
        logging.warning(f"MUST_JOIN check exception: {e}")
        return

    if not is_joined:
        if isinstance(chat_id, str) and not chat_id.startswith("-") and not chat_id.isdigit():
            link = f"https://t.me/{chat_id}"
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
