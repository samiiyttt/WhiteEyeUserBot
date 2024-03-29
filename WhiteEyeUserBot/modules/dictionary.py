"""Syntax: .meaning <word>"""

from PyDictionary import PyDictionary

from WhiteEyeUserBot import CMD_HELP
from WhiteEyeUserBot.utils import WhiteEye_on_cmd, edit_or_reply, sudo_cmd


@WhiteEye.on(WhiteEye_on_cmd("meaning (.*)"))
@WhiteEye.on(sudo_cmd("meaning (.*)", allow_sudo=True))
async def _(event):
    dayam = await edit_or_reply(event, "Finding Meaning.....")
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    dictionary = PyDictionary()
    a = dictionary.meaning(input_str)
    b = a.get("Noun")
    kaif = ""
    for x in b:
        kaif += x + "\n"
    await dayam.edit(
        f"<b> meaning of {input_str} is:-</b>\n {kaif}",
        parse_mode="HTML",
    )


CMD_HELP.update(
    {
        "dictionary": "**Dictionary**\
\n\n**Syntax : **`.meaning <word>`\
\n**Usage :** Get meaning and pronunciation of a word."
    }
)
