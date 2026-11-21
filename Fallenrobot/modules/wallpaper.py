import random
from urllib.parse import quote

import aiohttp
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from FallenRobot import pbot

##TO-DO


@pbot.on_message(filters.command(["wall", "wallpaper"]))
async def wall(_, message: Message):
    try:
        text = message.text.split(None, 1)[1]
    except IndexError:
        text = None
    if not text:
        return await message.reply_text("`Please give some query to search.`")
    m = await message.reply_text("`Searching for wallpapers...`")
    try:
        async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=20)
        ) as session:
            async with session.get(
                f"https://api.safone.me/wall?query={quote(text)}"
            ) as resp:
                results = (await resp.json())["results"]
        pick = random.choice(results[:4])
        await message.reply_photo(
            photo=pick["imageUrl"],
            caption=f"🥀 **ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ :** {message.from_user.mention}",
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("ʟɪɴᴋ", url=pick["imageUrl"])],
                ]
            ),
        )
        await m.delete()
    except Exception:
        await m.edit_text(f"ᴡᴀʟʟᴘᴀᴘᴇʀ ɴᴏᴛ ғᴏᴜɴᴅ ғᴏʀ : {text}")
