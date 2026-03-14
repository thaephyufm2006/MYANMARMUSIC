import os
from datetime import datetime
from unidecode import unidecode
from PIL import ImageDraw, Image, ImageFont, ImageChops
from pyrogram import *
from pyrogram.types import *
from logging import getLogger
from MYANMARMUSIC import LOGGER
from pyrogram.types import Message
from MYANMARMUSIC.misc import SUDOERS
from MYANMARMUSIC import app
from MYANMARMUSIC.utils.database import *
from MYANMARMUSIC.utils.database import db

try:
    wlcm = db.welcome
except:
    from MYANMARMUSIC.utils.database import welcome as wlcm

LOGGER = getLogger(__name__)

class temp:
    ME = None
    CURRENT = 2
    CANCEL = False
    MELCOW = {}
    U_NAME = None
    B_NAME = None

def circle(pfp, size=(450, 450)):
    pfp = pfp.resize(size, Image.LANCZOS).convert("RGBA")
    bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)
    mask = Image.new("L", bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(pfp.size, Image.LANCZOS)
    mask = ImageChops.darker(mask, pfp.split()[-1])
    pfp.putalpha(mask)
    return pfp

def welcomepic(pic, user, chat, id, uname):
    background = Image.open("MYANMARMUSIC/assets/welcome.png")
    pfp = Image.open(pic).convert("RGBA")
    pfp = circle(pfp)
    pfp = pfp.resize((450, 450)) 
    draw = ImageDraw.Draw(background)
    font = ImageFont.truetype('MYANMARMUSIC/assets/font.ttf', size=45)
    font2 = ImageFont.truetype('MYANMARMUSIC/assets/font.ttf', size=90)
    draw.text((65, 250), f'NAME : {unidecode(user)}', fill="#FF0000", font=font)
    draw.text((65, 340), f'ID : {id}', fill="#FF0000", font=font)
    draw.text((65, 430), f"Main Owner: @HANTHAR_1999", fill="#00BFFF", font=font)
    pfp_position = (767, 133)  
    background.paste(pfp, pfp_position, pfp)  
    background.save(f"downloads/welcome#{id}.png")
    return f"downloads/welcome#{id}.png"

@app.on_message(filters.command("welcome") & ~filters.private)
async def auto_state(_, message):
    usage = "<b>❖ ᴜsᴀɢᴇ ➥</b> /welcome [on|off]"
    if len(message.command) == 1:
        return await message.reply_text(usage)

    chat_id = message.chat.id
    user = await app.get_chat_member(message.chat.id, message.from_user.id)

    if user.status in (enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER):
        A = await wlcm.find_one({"chat_id": chat_id})
        state = message.text.split(None, 1)[1].strip().lower()

        if state == "on":
            if A and not A.get("disabled", False):
                return await message.reply_text("✦ Special Welcome Already Enabled")
            await wlcm.update_one({"chat_id": chat_id}, {"$set": {"disabled": False}}, upsert=True)
            await message.reply_text(f"✦ Enabled Special Welcome in {message.chat.title}")

        elif state == "off":
            if A and A.get("disabled", False):
                return await message.reply_text("✦ Special Welcome Already Disabled")
            await wlcm.update_one({"chat_id": chat_id}, {"$set": {"disabled": True}}, upsert=True)
            await message.reply_text(f"✦ Disabled Special Welcome in {message.chat.title}")

        else:
            await message.reply_text(usage)
    else:
        await message.reply("✦ Only Admins Can Use This Command")

@app.on_chat_member_updated(filters.group, group=-3)
async def greet_group(_, member: ChatMemberUpdated):
    chat_id = member.chat.id
    A = await wlcm.find_one({"chat_id": chat_id})

    if A and A.get("disabled", False):  
        return

    if (
        not member.new_chat_member
        or member.new_chat_member.status in {"banned", "left", "restricted"}
        or member.old_chat_member
    ):
        return

    user = member.new_chat_member.user if member.new_chat_member else member.from_user
    try:
        pic = await app.download_media(
            user.photo.big_file_id, file_name=f"pp{user.id}.png"
        )
    except AttributeError:
        pic = "MYANMARMUSIC/assets/upic.png"

    if (temp.MELCOW).get(f"welcome-{member.chat.id}") is not None:
        try:
            await temp.MELCOW[f"welcome-{member.chat.id}"].delete()
        except Exception as e:
            LOGGER.error(e)

    try:
        welcomeimg = welcomepic(
            pic, user.first_name, member.chat.title, user.id, user.username
        )
        temp.MELCOW[f"welcome-{member.chat.id}"] = await app.send_photo(
            member.chat.id,
            photo=welcomeimg,
            caption=f"""🇲🇲 <b>  𝐇𝐞𝐥𝐥𝐨, 𝐰𝐞𝐥𝐜𝐨𝐦𝐞 𝐟𝐚𝐦𝐢𝐥𝐲 𝐠𝐫𝐨𝐮𝐩.
🇲🇲 𝐓𝐡𝐚𝐧𝐤 𝐚 𝐥𝐨𝐭, 𝐟𝐨𝐫 𝐣𝐨𝐢𝐧 𝐠𝐫𝐨𝐮𝐩!</b>

              🎸🥁🥁🥁🎸
 
🌴 𝐍𝐀𝐌𝐄  : {user.mention}
🌸 𝐃𝐀𝐓𝐄  : {datetime.now().strftime('%Y-%m-%d')}
🌹 𝐃𝐚𝐲    : {datetime.now().strftime('%A')}
<b><u>အရာရာမှာပြည်စုံနေပေးမဲ့ အချစ်မှာတော့ ကံမကောင်းခဲ့တဲ့သူပါ </u>🥺</b>""",
                        reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🤍 ᴀᴅᴅ ᴍᴇ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ 🤍", url=f"https://t.me/{app.username}?startgroup=True")],
                [
                    InlineKeyboardButton("မြန်မာ 𓆩♡𓆪 𝑋 𝑀𝑢𝑠𝑖𝑐", url="https://t.me/myanmarbot_music"),
                    InlineKeyboardButton("အချစ်များ💞", url="https://t.me/myanmar_music_Bot2027")
                ],
                [InlineKeyboardButton("Premium Shop", url="https://t.me/HANTHAR_1999")]
                ]),
              )

    except Exception as e:
        LOGGER.error(e)

    try:
        os.remove(f"downloads/welcome#{user.id}.png")
        os.remove(f"downloads/pp{user.id}.png")
    except Exception:
        pass
