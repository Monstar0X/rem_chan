import html
import json
import re
from time import sleep
from typing import Optional
from urllib.parse import quote

import requests
from telegram import (
    CallbackQuery,
    Chat,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ParseMode,
    Update,
    User,
)
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    Filters,
    MessageHandler,
)
from telegram.utils.helpers import mention_html

import FallenRobot.modules.sql.chatbot_sql as sql
from FallenRobot import BOT_ID, BOT_NAME, BOT_USERNAME, dispatcher
from FallenRobot.modules.helper_funcs.chat_status import user_admin, user_admin_no_reply
from FallenRobot.modules.log_channel import gloggable


@user_admin_no_reply
@gloggable
def fallenrm(update: Update, context: CallbackContext) -> str:
    query: Optional[CallbackQuery] = update.callback_query
    user: Optional[User] = update.effective_user
    match = re.match(r"rm_chat\((.+?)\)", query.data)
    if match:
        chat: Optional[Chat] = update.effective_chat
        sql.set_fallen(chat.id)
        update.effective_message.edit_text(
            "{} ᴄʜᴀᴛʙᴏᴛ ᴅɪsᴀʙʟᴇᴅ ʙʏ {}.".format(
                dispatcher.bot.first_name, mention_html(user.id, user.first_name)
            ),
            parse_mode=ParseMode.HTML,
        )
        return (
            f"<b>{html.escape(chat.title or str(chat.id))}:</b>\n"
            f"AI_DISABLED\n"
            f"<b>Admin :</b> {mention_html(user.id, html.escape(user.first_name))}\n"
        )

    return ""


@user_admin_no_reply
@gloggable
def fallenadd(update: Update, context: CallbackContext) -> str:
    query: Optional[CallbackQuery] = update.callback_query
    user: Optional[User] = update.effective_user
    match = re.match(r"add_chat\((.+?)\)", query.data)
    if match:
        chat: Optional[Chat] = update.effective_chat
        sql.rem_fallen(chat.id)
        update.effective_message.edit_text(
            "{} ᴄʜᴀᴛʙᴏᴛ ᴇɴᴀʙʟᴇᴅ ʙʏ {}.".format(
                dispatcher.bot.first_name, mention_html(user.id, user.first_name)
            ),
            parse_mode=ParseMode.HTML,
        )
        return (
            f"<b>{html.escape(chat.title or str(chat.id))}:</b>\n"
            f"AI_ENABLE\n"
            f"<b>Admin :</b> {mention_html(user.id, html.escape(user.first_name))}\n"
        )

    return ""


@user_admin
@gloggable
def fallen(update: Update, context: CallbackContext):
    message = update.effective_message
    msg = "• ᴄʜᴏᴏsᴇ ᴀɴ ᴏᴩᴛɪᴏɴ ᴛᴏ ᴇɴᴀʙʟᴇ/ᴅɪsᴀʙʟᴇ ᴄʜᴀᴛʙᴏᴛ"
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="ᴇɴᴀʙʟᴇ", callback_data="add_chat({})"),
                InlineKeyboardButton(text="ᴅɪsᴀʙʟᴇ", callback_data="rm_chat({})"),
            ],
        ]
    )
    message.reply_text(
        text=msg,
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML,
    )


def fallen_message(context: CallbackContext, message):
    reply_message = message.reply_to_message
    if message.text.lower() == "fallen":
        return True
    elif BOT_USERNAME in message.text:
        return True
    elif reply_message:
        if reply_message.from_user and reply_message.from_user.id == BOT_ID:
            return True
    else:
        return False


def chatbot(update: Update, context: CallbackContext):
    message = update.effective_message
    chat_id = update.effective_chat.id
    bot = context.bot
    is_fallen = sql.is_fallen(chat_id)
    if is_fallen:
        return

    if message.text and not message.document:
        if not fallen_message(context, message):
            return
        bot.send_chat_action(chat_id, action="typing")
        try:
            request = requests.get(
                "https://kora-api.vercel.app/chatbot/2d94e37d-937f-4d28-9196-bd5552cac68b/"
                f"{quote(BOT_NAME, safe='')}/Anonymous/message={quote(message.text, safe='')}",
                timeout=15,
            )
            reply = json.loads(request.text).get("reply")
        except (requests.RequestException, ValueError, AttributeError):
            return
        if not reply:
            return
        sleep(0.5)
        message.reply_text(reply)


__help__ = f"""
*{BOT_NAME} has an chatbot which provides you a seemingless chatting experience :*

 »  /chatbot *:* Shows chatbot control panel
"""

__mod_name__ = "Cʜᴀᴛʙᴏᴛ"


CHATBOTK_HANDLER = CommandHandler("chatbot", fallen, run_async=True)
ADD_CHAT_HANDLER = CallbackQueryHandler(fallenadd, pattern=r"add_chat", run_async=True)
RM_CHAT_HANDLER = CallbackQueryHandler(fallenrm, pattern=r"rm_chat", run_async=True)
CHATBOT_HANDLER = MessageHandler(
    Filters.text
    & (~Filters.regex(r"^#[^\s]+") & ~Filters.regex(r"^!") & ~Filters.regex(r"^\/")),
    chatbot,
    run_async=True,
)

dispatcher.add_handler(ADD_CHAT_HANDLER)
dispatcher.add_handler(CHATBOTK_HANDLER)
dispatcher.add_handler(RM_CHAT_HANDLER)
dispatcher.add_handler(CHATBOT_HANDLER)

__handlers__ = [
    ADD_CHAT_HANDLER,
    CHATBOTK_HANDLER,
    RM_CHAT_HANDLER,
    CHATBOT_HANDLER,
]
