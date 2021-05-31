import importlib

from telegram import ParseMode
from telegram.ext import CommandHandler, Filters

from forwarder import API_KEY, OWNER_ID, WEBHOOK, IP_ADDRESS, URL, CERT_PATH, PORT, LOGGER, \
    updater, dispatcher
from forwarder.modules import ALL_MODULES

PM_START_TEXT = """
Olá {}, eu sou {}!
Este bot é destinado para envio de listas de Divulgação do Listão do Bem. Se você tem algo de bom para contribuir com seu canal/grupo, vem compartilhar junto com a gente! Inscreva-se aqui: @listaodobembot
"""

PM_HELP_TEXT = """
Aqui está a lista de comandos:
 - /start : iniciar o bot.
 - /help : envia essa mensagem.
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
        message.reply_text("I'm up and running!")


def help(update, context):
    chat = update.effective_chat  # type: Optional[Chat]
    message = update.effective_message  # type: Optional[Message]

    if not chat.type == "private":
        message.reply_text("Contact me via PM to get a list of usable commands.")
    else:
        message.reply_text(PM_HELP_TEXT)


def main():
    start_handler = CommandHandler("start", start, filters=Filters.user(OWNER_ID), run_async=True)
    help_handler = CommandHandler("help", help, filters=Filters.user(OWNER_ID), run_async=True)
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
