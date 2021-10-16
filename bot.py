import os, logging, asyncio
from telethon import Button
from telethon import TelegramClient, events
from telethon.tl.types import ChannelParticipantAdmin
from telethon.tl.types import ChannelParticipantCreator
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.errors import UserNotParticipantError

logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - [%(levelname)s] - %(message)s'
)
LOGGER = logging.getLogger(__name__)

api_id = int(os.environ.get("APP_ID"))
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("TOKEN")
client = TelegramClient('client', api_id, api_hash).start(bot_token=bot_token)
spam_chats = []

@client.on(events.NewMessage(pattern="^/start$"))
async def start(event):
  await event.reply("__**I'm MentionX Bot**, I can mention almost all members in group or channel 👻\nClick **/help** for more information__\n\n Need Any Help ? Follow [ELECTRO](https://t.me/ELECTRO_UPDATES) on Telegram.",
                    buttons=(
                      [Button.url('Channel🇮🇳', 'https://t.me/ELECTRO_UPDATES'),
                      Button.url('Group Support🇮🇳', 'https://t.me/ELECTROBOT_Support')]
                    ),
                    link_preview=False
                   )

@client.on(events.NewMessage(pattern="^/help$"))
async def help(event):
  helptext = "**Help Menu of MentionX Bot**\n\nCommand: /all\n__You can use this command with text what you want to mention others.__\n`Example: /all Good Morning!`\n__You can you this command as a reply to any message. Bot will tag users to that replied messsage__.\nCommand: /cancel\n__You can stop mentioning all users.__\n\n Need Any Help ? Follow [electro](https://t.me/BONDOFBESTIZZ) on Telegram."
  await event.reply(helptext,
                    buttons=(
                      [Button.url('Channel🇮🇳', 'https://t.me/ELECTRO_UPDATES'),
                      Button.url('Group Support🇮🇳', 'https://t.me/ELECTROBOT_SUPPORT')]
                    ),
                    link_preview=False
                   )
  
@client.on(events.NewMessage(pattern="^/all ?(.*)"))
async def mentionall(event):
  chat_id = event.chat_id
  if event.is_private:
    return await event.respond("__This command can be use in groups and channels!__")
  
  is_admin = False
  try:
    partici_ = await client(GetParticipantRequest(
      event.chat_id,
      event.sender_id
    ))
  except UserNotParticipantError:
    is_admin = False
  else:
    if (
      isinstance(
        partici_.participant,
        (
          ChannelParticipantAdmin,
          ChannelParticipantCreator
        )
      )
    ):
      is_admin = True
  if not is_admin:
    return await event.respond("__Only admins can mention all!__")
  
  if event.pattern_match.group(1) and event.is_reply:
    return await event.respond("__Give me one argument!__")
  elif event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.is_reply:
    mode = "text_on_reply"
    msg = await event.get_reply_message()
    if msg == None:
        return await event.respond("__I can't mention members for older messages! (messages which are sent before I'm added to group)__")
  else:
    return await event.respond("__Reply to a message or give me some text to mention others!__")
  
  spam_chats.append(chat_id)
  usrnum = 0
  usrtxt = ''
  async for usr in client.iter_participants(chat_id):
    if not chat_id in spam_chats:
      break
    usrnum += 1
    usrtxt += f"[{usr.first_name} ,](tg://user?id={usr.id}) "
    if usrnum == 5:
      if mode == "text_on_cmd":
        txt = f"{msg}\n\n\n{usrtxt}"
        await client.send_message(chat_id, txt)
      elif mode == "text_on_reply":
        await msg.reply(usrtxt)
      await asyncio.sleep(1)
      usrnum = 0
      usrtxt = ''
  try:
    spam_chats.remove(chat_id)
  except:
    pass

@client.on(events.NewMessage(pattern="^/cancel$"))
async def cancel_spam(event):
  if not event.chat_id in spam_chats:
    return await event.respond('__There is no proccess on going...__')
  else:
    try:
      spam_chats.remove(event.chat_id)
    except:
      pass
    return await event.reply("𝚂𝚝𝚘𝚙𝚙𝚎𝚍 𝙼𝚎𝚗𝚝𝚒𝚘𝚗𝚒𝚗𝚐...")

print(">> BOT STARTED <<")
client.run_until_disconnected()
