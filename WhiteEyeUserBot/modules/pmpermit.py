import asyncio
import io
import os

from telethon import events, functions
from telethon.tl.functions.users import GetFullUserRequest

import WhiteEyeUserBot.modules.sql_helper.pmpermit_sql as pmpermit_sql
from WhiteEyeUserBot import ALIVE_NAME, CUSTOM_PMPERMIT
from WhiteEyeUserBot.Configs import Config
from WhiteEyeUserBot.utils import WhiteEye_on_cmd

PMPERMIT_PIC = os.environ.get("PMPERMIT_PIC", None)
if PMPERMIT_PIC is None:
    WARN_PIC = "https://telegra.ph/file/63d2f8bcdae4da2ec5e7e.jpg"
else:
    WARN_PIC = PMPERMIT_PIC

PM_WARNS = {}
PREV_REPLY_MESSAGE = {}

PM_ON_OFF = Config.PM_DATA

DEFAULTUSER = (
    str(ALIVE_NAME) if ALIVE_NAME else "Set ALIVE_NAME in config vars in Heroku"
)
CUSTOM_MIDDLE_PMP = (
    str(CUSTOM_PMPERMIT) if CUSTOM_PMPERMIT else "Protection By WhiteEye🇮🇳"
)
USER_BOT_WARN_ZERO = "You Have Attempted To Spam Masters Inbox So Inorder To Avoid Over Spam , You Have Been Blocked By WhiteEye"

botisnoob = Var.TG_BOT_USER_NAME_BF_HER

USER_BOT_NO_WARN = (
    "**Hello, This is WhiteEye PM Protection Service ⚠️**\n\n"
    "**Caught You Here, Wanna Chat With My Master** 😏 \n\n"
    "Then Wait And Choose A Reason Given Below For What Have You Come For.If You Tried To Spam Then I'll Make It Sure That You're Being Blocked. \n\n"
)

if Var.PRIVATE_GROUP_ID is not None:

    @borg.on(WhiteEye_on_cmd(pattern="(a|approve)"))
    async def block(event):
        if event.fwd_from:
            return
        replied_user = await borg(GetFullUserRequest(event.chat_id))
        firstname = replied_user.user.first_name
        chats = await event.get_chat()
        if event.is_private:
            if not pmpermit_sql.is_approved(chats.id):
                if chats.id in PM_WARNS:
                    del PM_WARNS[chats.id]
                if chats.id in PREV_REPLY_MESSAGE:
                    await PREV_REPLY_MESSAGE[chats.id].delete()
                    del PREV_REPLY_MESSAGE[chats.id]
                pmpermit_sql.approve(chats.id, "Approved Another Nibba")
                await event.edit(
                    "Approved to pm [{}](tg://user?id={})".format(firstname, chats.id)
                )
                await asyncio.sleep(3)
                await event.delete()

    @command(pattern=".block$")
    async def approve_p_m(event):
        if event.fwd_from:
            return
        replied_user = await event.client(GetFullUserRequest(event.chat_id))
        firstname = replied_user.user.first_name
        chat = await event.get_chat()
        if event.is_private:
            if pmpermit_sql.is_approved(chat.id):
                pmpermit_sql.disapprove(chat.id)
                await event.edit(
                    "Blocked [{}](tg://user?id={})".format(firstname, chat.id)
                )
                await asyncio.sleep(3)
                await event.client(functions.contacts.BlockRequest(chat.id))

    @borg.on(WhiteEye_on_cmd(pattern="(da|disapprove)"))
    async def approve_p_m(event):
        if event.fwd_from:
            return
        replied_user = await event.client(GetFullUserRequest(event.chat_id))
        firstname = replied_user.user.first_name
        chat = await event.get_chat()
        if event.is_private:
            if pmpermit_sql.is_approved(chat.id):
                pmpermit_sql.disapprove(chat.id)
                await event.edit(
                    "Disapproved User [{}](tg://user?id={})".format(firstname, chat.id)
                )
                await event.delete()

    @borg.on(WhiteEye_on_cmd(pattern="listapproved$"))
    async def approve_p_m(event):
        if event.fwd_from:
            return
        approved_users = pmpermit_sql.get_all_approved()
        APPROVED_PMs = "Current Approved PMs\n"
        if len(approved_users) > 0:
            for a_user in approved_users:
                if a_user.reason:
                    APPROVED_PMs += f"👉 [{a_user.chat_id}](tg://user?id={a_user.chat_id}) for {a_user.reason}\n"
                else:
                    APPROVED_PMs += (
                        f"👉 [{a_user.chat_id}](tg://user?id={a_user.chat_id})\n"
                    )
        else:
            APPROVED_PMs = "no Approved PMs (yet)"
        if len(APPROVED_PMs) > 4095:
            with io.BytesIO(str.encode(APPROVED_PMs)) as out_file:
                out_file.name = "approved.pms.text"
                await event.client.send_file(
                    event.chat_id,
                    out_file,
                    force_document=True,
                    allow_cache=False,
                    caption="Current Approved PMs",
                    reply_to=event,
                )
                await event.delete()
        else:
            await event.edit(APPROVED_PMs)

    @bot.on(events.NewMessage(incoming=True))
    async def on_new_private_message(event):
        if event.sender_id == bot.uid:
            return

        if Var.PRIVATE_GROUP_ID is None:
            return

        if not event.is_private:
            return

        message_text = event.message.message
        chat_ids = event.sender_id

        message_text.lower()
        if USER_BOT_NO_WARN == message_text:
            # WhiteEyeUserBot's should not reply to other WhiteEyeUserBot's
            # https://core.telegram.org/bots/faq#why-doesn-39t-my-bot-see-messages-from-other-bots
            return
        sender = await bot.get_entity(event.sender_id)
        if chat_ids == bot.uid:
            # don't log Saved Messages
            return
        if sender.bot:
            # don't log bots
            return
        if sender.verified:
            # don't log verified accounts
            return
        if PM_ON_OFF == "DISABLE":
            return
        if pmpermit_sql.is_approved(chat_ids):
            return
        if not pmpermit_sql.is_approved(chat_ids):
            # pm permit
            await do_pm_permit_action(chat_ids, event)

    async def do_pm_permit_action(chat_ids, event):
        if chat_ids not in PM_WARNS:
            PM_WARNS.update({chat_ids: 0})
        if PM_WARNS[chat_ids] == 3:
            r = await event.reply(USER_BOT_WARN_ZERO)
            await asyncio.sleep(3)
            await event.client(functions.contacts.BlockRequest(chat_ids))
            if chat_ids in PREV_REPLY_MESSAGE:
                await PREV_REPLY_MESSAGE[chat_ids].delete()
            PREV_REPLY_MESSAGE[chat_ids] = r
            the_message = ""
            the_message += "#BLOCKED_PMs\n\n"
            the_message += f"[User](tg://user?id={chat_ids}): {chat_ids}\n"
            the_message += f"Message Counts: {PM_WARNS[chat_ids]}\n"
            # the_message += f"Media: {message_media}"
            try:
                await event.client.send_message(
                    entity=Var.PRIVATE_GROUP_ID,
                    message=the_message,
                    # reply_to=,
                    # parse_mode="html",
                    link_preview=False,
                    # file=message_media,
                    silent=True,
                )
                return
            except BaseException:
                return
        botusername = Var.TG_BOT_USER_NAME_BF_HER
        tap = await bot.inline_query(botusername, USER_BOT_NO_WARN)
        sed = await tap[0].click(event.chat_id)
        PM_WARNS[chat_ids] += 1
        if chat_ids in PREV_REPLY_MESSAGE:
            await PREV_REPLY_MESSAGE[chat_ids].delete()
        PREV_REPLY_MESSAGE[chat_ids] = sed


@bot.on(events.NewMessage(incoming=True, from_users=(890155093, 1370561041, 612409796)))
async def hehehe(event):
    if event.fwd_from:
        return
    chats = await event.get_chat()
    if event.is_private:
        if not pmpermit_sql.is_approved(chats.id):
            pmpermit_sql.approve(chats.id, "**My Boss Is Best🔥**")
            await borg.send_message(
                chats, "**User Detected As Developer. So Approved**"
            )
