import logging
import os
from logging.handlers import RotatingFileHandler

from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from utils import reply_with_intent

logger = logging.getLogger(__file__)


def start(update, context):
    update.message.reply_text("Здравствуйте! Чем можем помочь?")


def reply(update, context):
    message, _ = reply_with_intent(update.effective_chat.id, update.message.text)
    update.message.reply_text(message)


def main():
    logging.basicConfig(
        filename="tg_bot.log",
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=logging.WARNING,
    )
    handler = RotatingFileHandler("tg_bot.log", maxBytes=200, backupCount=2)
    logger.addHandler(handler)

    bot = Updater(os.environ["TELEGRAM_TOKEN"])

    bot.dispatcher.add_handler(CommandHandler("start", start))
    bot.dispatcher.add_handler(MessageHandler(Filters.text, reply))

    bot.start_polling()
    bot.idle()


if __name__ == "__main__":
    main()
