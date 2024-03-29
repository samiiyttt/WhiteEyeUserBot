"""Get Telegram Profile Picture and other information
Syntax: .info @username"""
import html

from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName
from telethon.utils import get_input_location

from WhiteEyeUserBot import CMD_HELP, sclient
from WhiteEyeUserBot.utils import WhiteEye_on_cmd, edit_or_reply, sudo_cmd


@WhiteEye.on(WhiteEye_on_cmd("info ?(.*)"))
@WhiteEye.on(sudo_cmd("info ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    replied_user, error_i_a = await get_full_user(event)
    if replied_user is None:
        await edit_or_reply(event, str(error_i_a))
        return False
    replied_user_profile_photos = await borg(
        GetUserPhotosRequest(
            user_id=replied_user.user.id, offset=42, max_id=0, limit=80
        )
    )
    replied_user_profile_photos_count = "None"
    try:
        replied_user_profile_photos_count = replied_user_profile_photos.count
    except AttributeError:
        pass
    user_id = replied_user.user.id
    first_name = html.escape(replied_user.user.first_name)
    if first_name is not None:
        first_name = first_name.replace("\u2060", "")
    last_name = replied_user.user.last_name
    last_name = (
        last_name.replace("\u2060", "") if last_name else ("Last Name not found")
    )
    user_bio = replied_user.about
    if user_bio is not None:
        user_bio = html.escape(replied_user.about)
    common_chats = replied_user.common_chats_count
    try:
        dc_id, location = get_input_location(replied_user.profile_photo)
    except Exception as e:
        dc_id = "Unknown."
        str(e)
    hmmyes = sclient.is_banned(user_id)
    if hmmyes.banned == True:
        oki = f"""<b>ANTISPAM INC BANNED:</b> <code>True</code> 
<b>Reason :</b> <code>{hmmyes.reason}</code>"""
    else:
        oki = " "
    shazam = replied_user_profile_photos_count
    caption = f"""<b>INFO<b>
<b>Telegram ID</b>: <code>{user_id}</code>
<b>Permanent Link</b>: <a href='tg://user?id={user_id}'>Click Here</a>
<b>First Name</b>: <code>{first_name}</code>
<b>Second Name</b>: <code>{last_name}</code>
<b>BIO</b>: <code>{user_bio}</code>
<b>DC ID</b>: <code>{dc_id}</code>
<b>NO OF PSS</b>: <code>{shazam}</code>
<b>IS RESTRICTED</b>: <code>{replied_user.user.restricted}</code>
<b>VERIFIED</b>: <code>{replied_user.user.verified}</code>
<b>IS A BOT</b>: <code>{replied_user.user.bot}</code>
<b>Groups in Common</b>: <code>{common_chats}</code>
{oki}
"""
    message_id_to_reply = event.message.reply_to_msg_id
    if not message_id_to_reply:
        message_id_to_reply = event.message.id
    await borg.send_message(
        event.chat_id,
        caption,
        reply_to=message_id_to_reply,
        parse_mode="HTML",
        file=replied_user.profile_photo,
        force_document=False,
        silent=True,
    )
    await event.delete()


async def get_full_user(event):
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.forward:
            replied_user = await event.client(
                GetFullUserRequest(
                    previous_message.forward.from_id
                    or previous_message.forward.channel_id
                )
            )
            return replied_user, None
        else:
            replied_user = await event.client(
                GetFullUserRequest(previous_message.from_id)
            )
            return replied_user, None
    else:
        input_str = None
        try:
            input_str = event.pattern_match.group(1)
        except IndexError as e:
            return None, e
        if event.message.entities is not None:
            mention_entity = event.message.entities
            probable_user_mention_entity = mention_entity[0]
            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user, None
            else:
                try:
                    user_object = await event.client.get_entity(input_str)
                    user_id = user_object.id
                    replied_user = await event.client(GetFullUserRequest(user_id))
                    return replied_user, None
                except Exception as e:
                    return None, e
        elif event.is_private:
            try:
                user_id = event.chat_id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user, None
            except Exception as e:
                return None, e
        else:
            try:
                user_object = await event.client.get_entity(int(input_str))
                user_id = user_object.id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user, None
            except Exception as e:
                return None, e


CMD_HELP.update(
    {
        "information": "**Information**\
\n\n**Syntax : **`.info <mention a username/reply to a message>`\
\n**Usage :** Gives you information about the username."
    }
)
