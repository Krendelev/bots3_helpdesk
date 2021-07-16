import logging
import os

from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from utils import get_logger, reply_with_intent


def start(update, context):
    update.message.reply_text("Здравствуйте! Чем можем помочь?")


def reply(update, context):
    try:
        message, _ = reply_with_intent(update.effective_chat.id, update.message.text)
        update.message.reply_text(message)
    except Exception as err:
        logger.error(err)


def main():
    bot = Updater(os.environ["TELEGRAM_TOKEN"])

    bot.dispatcher.add_handler(CommandHandler("start", start))
    bot.dispatcher.add_handler(MessageHandler(Filters.text, reply))

    bot.start_polling()
    bot.idle()


if __name__ == "__main__":
    logger = get_logger(__file__)
    main()
