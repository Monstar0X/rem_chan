# <============================================== IMPORTS =========================================================>
import aiohttp
from telethon import events

from Database.mongodb.toggle_mongo import is_nekomode_on, nekomode_off, nekomode_on
from FallenRobot import telethn as tbot

# <=======================================================================================================>
url_sfw = "https://api.waifu.pics/sfw/"
# Only categories that actually exist on api.waifu.pics/sfw
allowed_commands = [
    "waifu",
    "neko",
    "shinobu",
    "megumin",
    "bully",
    "cuddle",
    "cry",
    "hug",
    "awoo",
    "kiss",
    "lick",
    "pat",
    "smug",
    "bonk",
    "yeet",
    "blush",
    "smile",
    "wave",
    "highfive",
    "handhold",
    "nom",
    "bite",
    "glomp",
    "slap",
    "wink",
    "poke",
    "dance",
    "cringe",
]

# <================================================ FUNCTION =======================================================>
@tbot.on(events.NewMessage(pattern=r"(?i)^/nekomode(?:@\w+)? on$"))
async def enable_nekomode(event):
    await nekomode_on(event.chat_id)
    await event.reply("Nekomode has been enabled.")


@tbot.on(events.NewMessage(pattern=r"(?i)^/nekomode(?:@\w+)? off$"))
async def disable_nekomode(event):
    await nekomode_off(event.chat_id)
    await event.reply("Nekomode has been disabled.")


@tbot.on(
    events.NewMessage(
        pattern=r"(?i)^/({})(?:@\w+)?$".format("|".join(allowed_commands))
    )
)
async def nekomode_commands(event):
    if not await is_nekomode_on(event.chat_id):
        return
    target = event.pattern_match.group(1).lower()
    try:
        async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=15)
        ) as session:
            async with session.get(f"{url_sfw}{target}") as response:
                result = await response.json()
        animation_url = result["url"]
    except (aiohttp.ClientError, ValueError, KeyError, TimeoutError):
        return await event.reply("Couldn't fetch that right now, try again later.")

    await event.respond(file=animation_url)


__help__ = """
*✨ Sends fun Gifs/Images*

➥ /nekomode on : Enables fun neko mode.
➥ /nekomode off : Disables fun neko mode

» /bully: sends random bully gifs.
» /neko: sends random neko gifs.
» /highfive: sends random highfive gifs.
» /wave: sends random wave GIFs.
» /smile: sends random smile GIFs.
» /blush: sends random blush GIFs.
» /waifu: sends random waifu images.
» /kiss: sends random kissing GIFs.
» /cuddle: sends random cuddle GIFs.
» /cry: sends random cry GIFs.
» /bonk: sends random cuddle GIFs.
» /smug: sends random smug GIFs.
» /slap: sends random slap GIFs.
» /hug: get hugged or hug a user.
» /pat: pats a user or get patted.
» /dance: sends a random dance gif.
» /poke: sends a random poke gif.
» /wink: sends a random wink gif.
» /bite: sends random bite GIFs.
» /handhold: sends random handhold GIFs.
"""

__mod_name__ = "ɴᴇᴋᴏ"
# <================================================ END =======================================================>
