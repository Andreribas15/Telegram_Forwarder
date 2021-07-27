import importlib

from telegram import ParseMode
from telegram.ext import CommandHandler, Filters

from forwarder import API_KEY, OWNER_ID, WEBHOOK, IP_ADDRESS, URL, CERT_PATH, PORT, LOGGER, \
    updater, dispatcher
from forwarder.modules import ALL_MODULES

PM_START_TEXT = """
╭─── • 🔖 • ───╮

Cᴇɴᴛʀᴀʟ ᴅᴀs Lɪsᴛᴀs

Dɪᴠᴜʟɢᴀᴄ̧ᴀ̃ᴏ ɢʀᴀᴛᴜɪᴛᴀ ᴅᴇ ᴄᴀɴᴀɪs ᴇ́ᴛɪᴄᴏs ᴅᴏ ᴛᴇʟᴇɢʀᴀᴍ.
Eɴᴠɪᴇ ᴏ ʟɪɴᴋ ᴅᴇ sᴇᴜ ᴄᴀɴᴀʟ ᴘᴀʀᴀ @FaleConosobot ᴇ ғɪϙᴜᴇ ᴄɪᴇɴᴛᴇ ᴅᴇ ɴᴏssᴀs ᴄᴏɴᴅɪᴄ̧ᴏ̃ᴇs ᴅᴇ ᴅɪᴠᴜʟɢᴀᴄ̧ᴀ̃ᴏ

╰─── • 😉 • ───╯
"""

PM_HELP_TEXT = """
Aqui está a lista de comandos:
 - /start : iniciar o bot.
 - /help : envia essa mensagem.
 
 Developed by @Andre_Ribas
"""

for module in ALL_MODULES:
    importlib.import_module("forwarder.modules." + module)


def start(update, context):
    chat = update.effective_chat  # type: Optional[Chat]
    message = update.effective_message  # type: Optional[Message]
    user = update.effective_user  # type: Optional[User]

    if chat.type == "private":
        message.reply_text(PM_START_TEXT.format(user.first_name, dispatcher.bot.first_name), parse_mode=ParseMode.HTML)
    else:
        message.reply_text("Estou pronto e funcionando!")


def help(update, context):
    chat = update.effective_chat  # type: Optional[Chat]
    message = update.effective_message  # type: Optional[Message]

    if not chat.type == "private":
        message.reply_text("Contate-me via PM para obter uma lista de comandos utilizáveis.")
    else:
        message.reply_text(PM_HELP_TEXT)


def main():
    start_handler = CommandHandler("start", start, run_async=False)
    help_handler = CommandHandler("help", help, run_async=False)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)

    if WEBHOOK:
        LOGGER.info("Using webhooks.")
        updater.start_webhook(listen=IP_ADDRESS,
                              port=PORT,
                              url_path=API_KEY)

        if CERT_PATH:
            updater.bot.set_webhook(url=URL + API_KEY,
                                    certificate=open(CERT_PATH, 'rb'))
        else:
            updater.bot.set_webhook(url=URL + API_KEY)

    else:
        LOGGER.info("Using long polling.")
        updater.start_polling(timeout=15, read_latency=4)

    updater.idle()


if __name__ == '__main__':
    LOGGER.info("Successfully loaded modules: " + str(ALL_MODULES))
    main()
