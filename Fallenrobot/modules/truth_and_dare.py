import requests
from telegram import Update
from telegram.ext import CallbackContext

from FallenRobot import dispatcher
from FallenRobot.modules.disable import DisableAbleCommandHandler


def _get_question(kind: str):
    try:
        resp = requests.get(f"https://api.truthordarebot.xyz/v1/{kind}", timeout=10)
        return resp.json()["question"]
    except (requests.RequestException, ValueError, KeyError):
        return None


def truth(update: Update, context: CallbackContext):
    update.effective_message.reply_text(
        _get_question("truth") or "Couldn't fetch a truth right now, try again later."
    )


def dare(update: Update, context: CallbackContext):
    update.effective_message.reply_text(
        _get_question("dare") or "Couldn't fetch a dare right now, try again later."
    )


TRUTH_HANDLER = DisableAbleCommandHandler("truth", truth, run_async=True)
DARE_HANDLER = DisableAbleCommandHandler("dare", dare, run_async=True)

dispatcher.add_handler(TRUTH_HANDLER)
dispatcher.add_handler(DARE_HANDLER)


__help__ = """
*Truth & Dare*

 ❍ /truth *:* Sends a random truth string.
 ❍ /dare *:* Sends a random dare string.
"""

__mod_name__ = "Tʀᴜᴛʜ-Dᴀʀᴇ"
