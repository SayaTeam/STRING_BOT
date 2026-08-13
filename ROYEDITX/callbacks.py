import traceback

from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import UserNotParticipant

from config import MUST_JOIN, OWNER_ID
from ROYEDITX.generate import generate_session, ask_ques, buttons_ques


async def is_user_subscribed(bot: Client, user_id: int) -> bool:
    if not MUST_JOIN or user_id == OWNER_ID:
        return True
    raw = str(MUST_JOIN).strip().lstrip("@")
    if not raw:
        return True
    chat_id = int(raw) if (raw.startswith("-") or raw.isdigit()) else raw
    try:
        member = await bot.get_chat_member(chat_id, user_id)
        return member.status not in [ChatMemberStatus.LEFT, ChatMemberStatus.BANNED]
    except UserNotParticipant:
        return False
    except Exception:
        return True


@Client.on_callback_query(filters.regex(pattern=r"^(generate|pyrogram|pyrogram1|pyrogram_bot|telethon_bot|telethon)$"))
async def _callbacks(bot: Client, callback_query: CallbackQuery):
    if not await is_user_subscribed(bot, callback_query.from_user.id):
        await callback_query.answer("❖ ғɪʀsᴛʟʏ ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ᴊᴏɪɴ ᴏᴜʀ ᴄʜᴀɴɴᴇʟ @C4Botz ᴛᴏ ᴜsᴇ ᴛʜɪs ʙᴏᴛ !", show_alert=True)
        return

    query = callback_query.matches[0].group(1)
    if query == "generate":
        await callback_query.answer()
        await callback_query.message.reply(ask_ques, reply_markup=InlineKeyboardMarkup(buttons_ques))
    elif query.startswith("pyrogram") or query.startswith("telethon"):
        try:
            if query == "pyrogram":
                await callback_query.answer()
                await generate_session(bot, callback_query.message)
            elif query == "pyrogram1":
                await callback_query.answer()
                await generate_session(bot, callback_query.message, old_pyro=True)
            elif query == "pyrogram_bot":
                await callback_query.answer("⬤ ᴛʜᴇ sᴇssɪᴏɴ ɢᴇɴᴇʀᴀᴛᴇᴅ ᴡɪʟʟ ʙᴇ ᴏғ ᴩʏʀᴏɢʀᴀᴍ ᴠ2.", show_alert=True)
                await generate_session(bot, callback_query.message, is_bot=True)
            elif query == "telethon_bot":
                await callback_query.answer()
                await generate_session(bot, callback_query.message, telethon=True, is_bot=True)
            elif query == "telethon":
                await callback_query.answer()
                await generate_session(bot, callback_query.message, telethon=True)
        except Exception as e:
            print(traceback.format_exc())
            print(e)
            await callback_query.message.reply(ERROR_MESSAGE.format(str(e)))


ERROR_MESSAGE = "⬤ ᴡᴛғ ! sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ. \n\n**● ᴇʀʀᴏʀ** ➥ {} " \
            "\n\n⬤ ᴩʟᴇᴀsᴇ ғᴏʀᴡᴀʀᴅ ᴛʜɪs ᴍᴇssᴀɢᴇ ᴛᴏ ➥ @C4Botz**, ɪғ ᴛʜɪs ᴍᴇssᴀɢᴇ " \
            "⬤ ᴅᴏᴇsɴ'ᴛ ᴄᴏɴᴛᴀɪɴ ᴀɴʏ sᴇɴsɪᴛɪᴠᴇ ɪɴғᴏʀᴍᴀᴛɪᴏɴ " \
            "⬤ ʙᴇᴄᴀᴜsᴇ ᴛʜɪs ᴇʀʀᴏʀ ɪs **ɴᴏᴛ ʟᴏɢɢᴇᴅ ʙʏ ᴛʜᴇ ʙᴏᴛ** !"
