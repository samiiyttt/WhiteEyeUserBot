# Copyright (c) By Midhun KM [@StarkXD]
# I Am Noob
# Official Web : nekobot.xyz
# "Copy It As You Want But Don't Edit Credits"
import requests

from WhiteEyeUserBot import CMD_HELP
from WhiteEyeUserBot.utils import WhiteEye_on_cmd, edit_or_reply, sudo_cmd


@WhiteEye.on(WhiteEye_on_cmd("ttt ?(.*)"))
@WhiteEye.on(sudo_cmd("ttt ?(.*)", allow_sudo=True))
async def noobishere(event):
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    reply = await event.get_reply_message()
    if event.pattern_match.group(1):
        ipman = event.pattern_match.group(1)
    elif reply.text:
        ipman = reply.message
    else:
        await edit_or_reply(event, "Trump : What Should I Tweet For You ?")
        return

    url = f"https://nekobot.xyz/api/imagegen?type=trumptweet&text={ipman}"
    starkgang = requests.get(url=url).json()
    meikobot = starkgang.get("message")
    tweetimg = meikobot
    starkxd = f"Trump Has Tweeted {ipman}"
    await edit_or_reply(event, "Trump : Wait I Am Tweeting Your Texts")
    await event.client.send_file(
        event.chat_id, tweetimg, caption=starkxd, reply_to=reply_to_id
    )


@WhiteEye.on(WhiteEye_on_cmd("tweet ?(.*)"))
@WhiteEye.on(sudo_cmd("tweet ?(.*)", allow_sudo=True))
async def noobishere(event):
    reply_to_id = event.message.id
    text = event.pattern_match.group(1)
    input_str = event.pattern_match.group(1)
    if text:
        if ":" in text:
            stark = input_str.split(":", 1)
        else:
            await event.reply(
                "You Are Using Invalid Syntax ! Make Sure To Use tweetusername:text Regex"
            )
            return
    if len(stark) != 2:
        await event.reply(
            "You Are Using Invalid Syntax ! Make Sure To Use tweetusername:text Regex"
        )
        return

    starky = stark[0]
    ipman = stark[1]
    url = f"https://nekobot.xyz/api/imagegen?type=tweet&username={starky}&text={ipman}"
    starkgang = requests.get(url=url).json()
    meikobot = starkgang.get("message")
    tweetimg = meikobot
    starkxd = f"{starky} Has Tweeted {ipman}"
    await edit_or_reply(event, f"{starky} : Wait I Am Tweeting Your Texts")
    await event.client.send_file(
        event.chat_id, tweetimg, caption=starkxd, reply_to=reply_to_id
    )


CMD_HELP.update(
    {
        "nekobot": "**NekoBot**\
\n\n**Syntax : **`.tweet<name> <text>, .ttt <text>`\
\n**Usage :** Fake Tweeting Plugin"
    }
)
